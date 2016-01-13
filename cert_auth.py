import pickle, rsa, os

if __name__ == "__main__":
    master_tup = pickle.load(open("masterKey.pickle", "rb"))
    master_key = rsa.PrivateKey(*master_tup)

    if os.path.exists("to_sign"):
        for key in os.listdir("." + os.sep + "to_sign"):
            tup = pickle.load(open("to_sign" + os.sep + key, "rb"))
            signed = rsa.sign(str(tup), master_key, "SHA-256")
            print("Key " + str(key) + " signed")
            print("Signiture valid? " + str(rsa.verify(str(tup), signed, master_key)))
            if not os.path.exists("signed"):
                os.mkdir("signed")
            pickle.dump(signed, open("signed" + os.sep + key, "wb"), 0)


def exportProof(priv):
    tup = (priv.n, priv.e)
    proof = rsa.sign(str(tup), priv,"SHA-256")
    print("Post this proof somewhere associated with your")
    print("organization, to verify your identity.")
    print("Send that link to gappleto97+development@gmail.com")
    return (tup,proof)
