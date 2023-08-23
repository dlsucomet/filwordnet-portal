from sklearn.decomposition import PCA


def sanitize_embeddings(embeddings):
    if embeddings:
        if embeddings != 'nan':
            embeddings = embeddings[1:-1]
            embeddings = embeddings.split()
            embeddings = [eval(e.strip())
                          for e in embeddings]  # change string to float

            return embeddings

    return ''


def load_embeddings(embeddings_list):
    if embeddings_list:

        pca = PCA(n_components=3)

        return pca.fit_transform(embeddings_list)

    return ''
