# Minimal Repro for Bazel `rules_proto_grpc_python` Patching Issue

This repository demonstrates an issue with patching the `rules_proto_grpc_python` module in a Bazel workspace. Specifically, the patch appears to be applied, but its effects are not reflected in the loaded module's dependencies or behavior.

---

## Problem Summary

When attempting to override the Python dependencies of the `rules_proto_grpc_python` module using a patch, the changes do not seem to take effect. The patched `MODULE.bazel` file contains the `breakplease` marker from the patch, indicating the patch was applied, but:

1. The `rules_proto_grpc_python` module appears to have already been loaded before the patch takes effect.
2. Overrides specified in the patch are not used in the runtime dependencies.

This leads to runtime vs. codegen mismatches because the patched Python requirements are not respected.

## Steps to Reproduce

1. Clone this repository and navigate to the root directory.
2. Build the project using Bazel:
   ```bash
   bazel build //:server
   ```
3. Observe that the `breakplease` marker is present in the patched `MODULE.bazel` file in the output base, but nothing crashes, indicating the patch is perhaps applied after the module is already loaded.
4. Note that the whole goal of this is to run `bazel run //:grpc_server` and have it not get upset about out of date python runtime dependencies.
