from predicter import reactions_predicter
import sqlite3
import pandas as pd


def get_reactions(text: str):
    predicter = reactions_predicter()


def read_posts_from_db(database_path, table_name):
    db_con = sqlite3.connect(f"{database_path}")
    cur = db_con.cursor()
    cur.execute(
        f"""
        SELECT p.post_id, p.post_text, GROUP_CONCAT(emoji || count) AS reactions_dictionary
    FROM {table_name} p
    INNER JOIN reactions r ON p.post_id = r.post_id
    GROUP BY p.post_id, post_text;
    """
    )
    data = pd.DataFrame(cur.fetchall(), columns=["post_id", "post_text", "reactions"])
    data = data.iloc[1:, :]
    data = data.set_index("post_id")
    return data


def main():
    posts_with_reactions = read_posts_from_db("db/database.db", "posts")
    rp = reactions_predicter(posts_with_reactions, "reactions")
    print(rp.predict(text="кормен - лучшая книга по алгоритмам"))
    print(rp.predict(text="террористы взяли в заложники автобус"))


main()
