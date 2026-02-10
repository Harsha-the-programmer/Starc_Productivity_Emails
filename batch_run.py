import time
from datetime import datetime
from main import run_once

REQUESTS_PER_CYCLE = 25
CYCLE_COUNT = 5
CYCLE_DURATION = 60
COOLDOWN_DURATION = 60

OUTPUT_FILE = "generated_emails.txt"


def run_batch():
    print("Starting batch execution")
    print(f"{CYCLE_COUNT} cycles")
    print(f"{REQUESTS_PER_CYCLE} requests per cycle\n")

    delay = CYCLE_DURATION / REQUESTS_PER_CYCLE

    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        for cycle in range(1, CYCLE_COUNT + 1):
            print(f"\nCycle {cycle} started")

            cycle_start = time.time()

            for i in range(1, REQUESTS_PER_CYCLE + 1):
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                email, error = run_once()

                f.write("\n" + "=" * 60 + "\n")
                f.write(f"Cycle: {cycle}, Request: {i}\n")
                f.write(f"Timestamp: {timestamp}\n\n")

                if error:
                    f.write(f"ERROR: {error}\n")
                    print(f"Cycle {cycle}, Req {i} failed")
                else:
                    f.write(email + "\n")
                    print(f"Cycle {cycle}, Req {i} done")

                time.sleep(delay)

            elapsed = time.time() - cycle_start
            print(f"Cycle {cycle} completed in {round(elapsed, 2)} seconds")

            if cycle < CYCLE_COUNT:
                print(f"Cooling down for {COOLDOWN_DURATION} seconds\n")
                time.sleep(COOLDOWN_DURATION)

    print("\nAll emails stored in:", OUTPUT_FILE)
    print("Batch execution finished")


if __name__ == "__main__":
    run_batch()
