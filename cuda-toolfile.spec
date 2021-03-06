### RPM external cuda-toolfile 2.0
Requires: cuda
%prep

%build

%install

mkdir -p %{i}/etc/scram.d
cat << \EOF_TOOLFILE >%{i}/etc/scram.d/cuda-stubs.xml
<tool name="cuda-stubs" version="@TOOL_VERSION@">
  <info url="https://developer.nvidia.com/cuda-toolkit"/>
  <lib name="cuda"/>
  <client>
    <environment name="CUDA_STUBS_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR"          default="$CUDA_STUBS_BASE/lib64/stubs"/>
  </client>
  <flags SKIP_TOOL_SYMLINKS="1"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%{i}/etc/scram.d/cuda.xml
<tool name="cuda" version="@TOOL_VERSION@">
  <info url="https://developer.nvidia.com/cuda-toolkit"/>
  <use name="cuda-stubs"/>
  <lib name="cudart"/>
  <lib name="nppc"/>
  <lib name="nvToolsExt"/>
  <client>
    <environment name="CUDA_BASE" default="@TOOL_ROOT@"/>
    <environment name="NVCC"      default="$CUDA_BASE/bin/nvcc"/>
    <environment name="BINDIR"    default="$CUDA_BASE/bin"/>
    <environment name="LIBDIR"    default="$CUDA_BASE/lib64"/>
    <environment name="INCLUDE"   default="$CUDA_BASE/include"/>
  </client>
  <flags CUDA_CFLAGS="-fPIC"/>
  <flags CUDA_FLAGS="-gencode arch=compute_35,code=sm_35 -gencode arch=compute_50,code=sm_50 -gencode arch=compute_61,code=sm_61"/>
  <runtime name="PATH" value="$CUDA_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
