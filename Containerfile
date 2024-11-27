FROM registry.access.redhat.com/ubi9/python-312 AS base

ENV PROW_JOBS_OUT_PATH="/tmp/prow_jobs.json"
ENV PROW_BASE_URL="https://prow.ci.openshift.org"
ENV PROW_JOBS_JSON_ENDPOINT="/prowjobs.js?omit=annotations%2Clabels%2Cdecoration_config%2Cpod_spec"

USER 0
ADD app-src /tmp/src
RUN /usr/bin/fix-permissions /tmp/src
USER 1001
RUN /usr/libexec/s2i/assemble

FROM base as fetch_prow_jobs
ENV APP_FILE="fetch_prow_jobs.py"
RUN /usr/libexec/s2i/run

FROM base AS unpack_prow_jobs
COPY --from=fetch_prow_jobs $PROW_JOBS_OUT_PATH /tmp/prow_jobs.json
ENV APP_FILE="unpack_prow_jobs.py"
ENV PROW_JOBS_JSON_PATH="/tmp/prow_jobs.json"
ENV UNPACKED_PROW_DIR="/tmp/prow"
ENV JOB_NAME_FILTER_REGEX="^periodic-.+-ocp4\.18-lp-interop-"
RUN /usr/libexec/s2i/run

FROM unpack_prow_jobs AS add_scripts
COPY --from=unpack_prow_jobs /tmp/prow/jobs /tmp/prow/jobs
ADD app-src/job_scripts /tmp/prow/job_scripts
ADD app-src/build_scripts /tmp/prow/build_scripts
ENV JOB_SCRIPTS_DIR="/tmp/prow/job_scripts"
ENV BUILD_SCRIPTS_DIR="/tmp/prow/build_scripts"
ENV APP_FILE="add_scripts.py"
RUN <<EOF 
    for d in /tmp/prow/jobs/by-job-name/*; do    
        link $d/$(ls $d -Xr | head -n 1) $d/latest
    done
EOF
RUN /usr/libexec/s2i/run



FROM registry.access.redhat.com/ubi9/ubi-minimal AS run
COPY --from=add_scripts /tmp/prow /tmp/prow
ADD app-src/requirements.txt /tmp/src/requirements.txt
WORKDIR /tmp/prow/jobs/by-job-name
RUN <<EOF
    microdnf install python312 python3.12-pip -y
    microdnf clean all
    python3.12 -m pip install -r /tmp/src/requirements.txt
EOF
CMD [ "/bin/bash" ]

