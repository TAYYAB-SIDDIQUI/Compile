
import os
import shutil
import py_compile

SOURCE_DIR = r"E:\Digi\VCIP_AUDITOR/VCIP_COMP_V2"
OUTPUT_DIR = r"E:\Digi\VCIP_AUDITOR_PYC_V2"


def compile_project(source_dir, output_dir):
    source_dir = os.path.abspath(source_dir)
    output_dir = os.path.abspath(output_dir)

    # Prevent output folder from being processed if it's inside source
    output_dir_with_sep = output_dir + os.sep

    for root, dirs, files in os.walk(source_dir):

        # Don't enter output directory
        dirs[:] = [
            d for d in dirs
            if not os.path.abspath(os.path.join(root, d)).startswith(output_dir_with_sep)
        ]

        relative_dir = os.path.relpath(root, source_dir)

        if relative_dir == ".":
            destination_dir = output_dir
        else:
            destination_dir = os.path.join(output_dir, relative_dir)

        os.makedirs(destination_dir, exist_ok=True)

        for file in files:

            source_file = os.path.join(root, file)

            # =========================================================
            # PYTHON FILE → COMPILE TO PYC
            # =========================================================
            if file.lower().endswith(".py"):

                pyc_name = os.path.splitext(file)[0] + ".pyc"
                output_file = os.path.join(destination_dir, pyc_name)

                try:
                    py_compile.compile(
                        source_file,
                        cfile=output_file,
                        doraise=True
                    )

                    print(f"[PYC] {source_file}")
                    print(f"      -> {output_file}")

                except Exception as e:
                    print(f"[ERROR] Failed to compile:")
                    print(f"        {source_file}")
                    print(f"        {e}")

            # =========================================================
            # ALL OTHER FILES → COPY AS-IS
            # =========================================================
            else:

                destination_file = os.path.join(destination_dir, file)

                try:
                    shutil.copy2(source_file, destination_file)

                    print(f"[COPY] {source_file}")
                    print(f"       -> {destination_file}")

                except Exception as e:
                    print(f"[ERROR] Failed to copy:")
                    print(f"        {source_file}")
                    print(f"        {e}")


if __name__ == "__main__":

    print("=" * 70)
    print("PYTHON PROJECT COMPILER")
    print("=" * 70)

    print(f"\nSOURCE : {SOURCE_DIR}")
    print(f"OUTPUT : {OUTPUT_DIR}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    compile_project(SOURCE_DIR, OUTPUT_DIR)

    print("\n" + "=" * 70)
    print("DONE")
    print("=" * 70)
