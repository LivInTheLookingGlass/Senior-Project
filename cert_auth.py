import pickle, rsa, os

if __name__ == "__main__":
    master_tup = pickle.load(open("." + os.sep + "masterKey.pickle","rb"))
    master_key = rsa.PrivateKey(*master_tup)

    if os.path.exists("to_sign"):
        for key in os.listdir("." + os.sep + "to_sign"):
            tup = pickle.load(open("." + os.sep + "to_sign" + os.sep + key,"rb"))
            signed = rsa.sign(str(tup),master_key,"SHA-256")
            print("Key " + str(key) + " signed")
            print("Signiture valid? " + str(rsa.verify(str(tup),signed,master_key)))
            if not os.path.exists("signed"):
                os.mkdir("signed")
            pickle.dump(signed,open("." + os.sep + "signed" + os.sep + key,"wb"),0)

def exportProof(priv):
    tup = (priv.n,priv.e)
    proof = rsa.sign(str(tup),priv,"SHA-256")
    pickle.dump(tup,open("key_to_send.pickle","wb"))
    print("Post this proof somewhere associated with your organization, to verify your identity. Send that link to gappleto97+development@gmail.com, along with the pickled copy of your public key that this will generate. Rename it to match your organization's name")
    return proof
