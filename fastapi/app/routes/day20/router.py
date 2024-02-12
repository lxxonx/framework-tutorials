import os
import subprocess
import tarfile
from tempfile import TemporaryDirectory, TemporaryFile
from fastapi import APIRouter, Request, Response

day_20_router = APIRouter(prefix="/20")


@day_20_router.post("/archive_files")
async def archive_files(request: Request):
    byte_file: list[bytes] = await request.body()

    with TemporaryFile() as temp_file:
        temp_file.write(byte_file)
        temp_file.seek(0)
        with tarfile.open(fileobj=temp_file, mode="r") as tar:
            members = tar.getmembers()
            return len(members)


@day_20_router.post("/archive_files_size")
async def archive_files_size(request: Request):
    byte_file: list[bytes] = await request.body()
    with TemporaryFile() as temp_file:
        temp_file.write(byte_file)
        temp_file.seek(0)
        with tarfile.open(fileobj=temp_file, mode="r") as tar:
            members = tar.getmembers()
            total_size = sum(member.size for member in members)
            return total_size


@day_20_router.post("/cookie")
async def cookie_read(request: Request):
    byte_file: list[bytes] = await request.body()
    with TemporaryFile() as temp_file:
        temp_file.write(byte_file)
        temp_file.seek(0)
        with TemporaryDirectory() as temp_dir:
            with tarfile.open(fileobj=temp_file, mode="r") as tar:
                tar.extractall(path=temp_dir)
                BRANCH = "christmas"
                output = subprocess.check_output(
                    ["git", "log", "--format=%cn,%H", BRANCH],
                    cwd=temp_dir,
                )
                output = output.decode("utf-8").splitlines()
                output = [line.split(",") for line in output]

                for [author, commit_hash] in output:
                    subprocess.check_output(
                        ["git", "checkout", commit_hash, "--force"], cwd=temp_dir
                    )
                    for path, _, file in os.walk(temp_dir):
                        if "santa.txt" in file:
                            with open(f"{path}/santa.txt") as f:
                                file_str = f.read()

                                if "COOKIE" in file_str:
                                    return Response(
                                        content=f"{author} {commit_hash}",
                                        status_code=200,
                                    )
