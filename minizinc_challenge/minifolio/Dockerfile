FROM minizinc/mznc2026:latest

ENV DEBIAN_FRONTEND=noninteractive
ENV MINIZINC_VERSION=2.9.7

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
      ca-certificates \
      wget \
      git \
      python3 \
      python3-click \
      python3-psutil \
      make \
      g++ \
      flex \
      bison \
      file \
      xz-utils \
      libgl1 \
      libegl1 \
      libfontconfig1 \
      libfreetype6 && \
    rm -rf /var/lib/apt/lists/*

# Install the full MiniZinc bundle alongside the Challenge MiniZinc.
# We keep the Challenge 'minizinc' command as the default driver.
RUN wget -O /tmp/minizinc.tgz \
      "https://github.com/MiniZinc/MiniZincIDE/releases/download/${MINIZINC_VERSION}/MiniZincIDE-${MINIZINC_VERSION}-bundle-linux-x86_64.tgz" && \
    mkdir -p /opt && \
    tar -xzf /tmp/minizinc.tgz -C /opt && \
    mv "/opt/MiniZincIDE-${MINIZINC_VERSION}-bundle-linux-x86_64" /opt/minizinc-bundle && \
    rm /tmp/minizinc.tgz

# Put bundle binaries later in PATH:
# - 'minizinc' remains the Challenge driver from minizinc/mznc2026
# - fzn-gecode, fzn-chuffed, cp-sat helpers etc. are still discoverable
ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/minizinc-bundle/bin"

# Tell the Challenge MiniZinc driver where to find bundled solver configs,
# but keep org.minizinc.mznc as the default solver.
RUN mkdir -p /root/.minizinc && \
    printf '%s\n' \
      '{' \
      '  "mzn_solver_path": ["/opt/minizinc-bundle/share/minizinc/solvers"],' \
      '  "tagDefaults": [["", "org.minizinc.mznc"]]' \
      '}' \
      > /root/.minizinc/Preferences.json

# Install mzn2feat.
RUN git clone --depth 1 https://github.com/CP-Unibo/mzn2feat.git /opt/mzn2feat && \
    cd /opt/mzn2feat && \
    bash install --no-xcsp

ENV PATH="/opt/mzn2feat/bin:${PATH}"

# Install SUNNY-CP.
RUN git clone --depth 1 https://github.com/CP-Unibo/sunny-cp.git /opt/sunny-cp && \
    cd /opt/sunny-cp && \
    bash install.sh

ENV SUNNY_HOME="/opt/sunny-cp"
ENV PATH="/opt/sunny-cp/bin:${PATH}"

COPY minifolio /usr/local/bin/minifolio

RUN chmod +x /usr/local/bin/minifolio && \
    printf '%s\n' \
      '#!/usr/bin/env bash' \
      'set -euo pipefail' \
      'exec /usr/local/bin/minifolio "$@"' \
      > /minizinc/mzn-exec-fd && \
    printf '%s\n' \
      '#!/usr/bin/env bash' \
      'set -euo pipefail' \
      'exec /usr/local/bin/minifolio "$@"' \
      > /minizinc/mzn-exec-free && \
    printf '%s\n' \
      '#!/usr/bin/env bash' \
      'set -euo pipefail' \
      'exec /usr/local/bin/minifolio "$@"' \
      > /minizinc/mzn-exec-par && \
    chmod +x /minizinc/mzn-exec-fd /minizinc/mzn-exec-free /minizinc/mzn-exec-par && \
    ln -sf /minizinc/mzn-exec-fd /usr/local/bin/mzn-exec-fd && \
    ln -sf /minizinc/mzn-exec-free /usr/local/bin/mzn-exec-free && \
    ln -sf /minizinc/mzn-exec-par /usr/local/bin/mzn-exec-par

# Build-time sanity checks.
RUN command -v minizinc && \
    minizinc --solvers && \
    command -v sunny-cp && \
    command -v minifolio && \
    ldd /opt/minizinc-bundle/bin/fzn-gecode | grep "not found" && exit 1 || true

WORKDIR /work
