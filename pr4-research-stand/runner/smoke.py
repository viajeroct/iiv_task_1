import subprocess, time, requests
def sh(*a): return subprocess.run(a, check=True, capture_output=True, text=True).stdout
sh("docker", "compose", "up", "-d", "--build", "db", "sut")
time.sleep(20)
r = requests.get("http://localhost:8000/api/items/42", timeout=5)
assert r.status_code == 200, r.status_code
print("SUT ответил:", r.json())
print("SMOKE OK")
