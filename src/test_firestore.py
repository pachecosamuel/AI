from utils.firebase import db

def test_firestore():
    users_ref = db.collection("users")
    docs = users_ref.stream()

    for doc in docs:
        print(f"{doc.id} => {doc.to_dict()}")


test_firestore()
# if __name__ == "__main__":
#     test_firestore()
