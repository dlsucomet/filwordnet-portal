from sklearn.decomposition import PCA


def load_embeddings(embeddings_list):
    if embeddings_list:

        pca = PCA(n_components=3)

        return pca.fit_transform(embeddings_list)

    return ''
