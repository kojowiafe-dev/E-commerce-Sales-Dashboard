from api.dbloader import load_csv_to_db
import asyncio


if __name__ == "__main__":
    asyncio.run(load_csv_to_db("./data/all_data_cleaned.csv"))