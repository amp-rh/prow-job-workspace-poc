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
ENV JOB_NAME_FILTER_REGEX=".+-ocp4\.18-lp-interop-"
RUN /usr/libexec/s2i/run

FROM unpack_prow_jobs AS link_latest
WORKDIR $UNPACKED_PROW_DIR/jobs/by-job-name
RUN <<EOF 
    for d in ./*; do    
        link $d/$(ls $d -Xr | head -n 1) $d/latest
    done
EOF

FROM link_latest AS run
WORKDIR $UNPACKED_PROW_DIR/jobs
CMD [ "/bin/bash" ]

