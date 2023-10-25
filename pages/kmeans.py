#import libs

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#from kneed import KneeLocator
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D

from pandas.plotting import scatter_matrix 
from sklearn.metrics import silhouette_score
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def process_customer():
    data = pd.read_csv("assets/customers.csv")
    del(data["CustomerID"])
    cons = data.iloc[:,1:]

    #Standardize Data
    scaler = StandardScaler().fit(cons.values)
    features = scaler.transform(cons.values)
    scaled_data = pd.DataFrame(features, columns = cons.columns)
    scaled_data.head()
    
    #create dummies for categorical variables
    gen = data["Gender"]
    cons_data = scaled_data.join(gen)
    cons_data = pd.get_dummies(cons_data, prefix = None, prefix_sep = "_", dummy_na = False,
                              columns = None, sparse = False, drop_first = False, dtype = None)
    cons_data = cons_data.drop(["Gender_Male"], axis = 1)

    return cons_data


def build_model(cons_data, optimal_k, pca = False):
    
    data = pd.read_csv("assets/customers.csv")
    
    if pca:
        pca = PCA(n_components = len(cons_data.columns))
        principalComponents = pca.fit_transform(cons_data)

        feat = range(pca.n_components_)
        PCA_components = pd.DataFrame(principalComponents)
        
        rang = range(1, 10)
        inertias = []

        for ra in rang:
            model = KMeans(n_clusters= ra)
            model.fit(PCA_components.iloc[:,:1])
            inertias.append(model.inertia_)

        #create dataframe
        cons_df = pd.DataFrame({"Cluster" : range(1,10), "SSE" : inertias})
        
        #Plot Graph
        elbow_fig = make_subplots(rows=1, cols=2)
        
        #feature_selection
        elbow_fig.add_trace(
            go.Bar( x=list(feat), y=pca.explained_variance_ratio_.round(2),
                    text=pca.explained_variance_ratio_.round(2),
                    textposition='auto',
                ),
            row=1, col=1
        )
        
        #elbow
        elbow_fig.add_trace(
            go.Scatter(x=cons_df['Cluster'], y=cons_df['SSE'],
                            mode='markers+lines',
                            name='markers'),
            row=1, col=2
        )

        elbow_fig.update_layout(height=400, width=1200, title_text="Feature Selection and Optimal K selection using Elbow Method")

        #Build model with 4 cluster
        kmeans = KMeans(n_clusters = optimal_k)
        kmeans.fit(PCA_components.iloc[:,:1])

        #Evaluate Model
        sil = silhouette_score(PCA_components.iloc[:,:2], kmeans.labels_, metric='euclidean')
        
        clusters = kmeans.fit_predict(PCA_components.iloc[:,:2])
        cons_data["label"] = clusters
        
        #plot 3D fig
        fig = go.Figure(data=[go.Scatter3d(
            x=cons_data['Age'],
            y=cons_data['Annual Income (k$)'],
            z=cons_data['Spending Score (1-100)'],
            mode='markers',
            marker=dict(
                size=4,
                color=cons_data['label'],  # set color to an array/list of desired values
                colorscale='Viridis',   # choose a colorscale
                opacity=0.8
            ),
        )])

        # tight layout
        fig.update_layout(
            #margin=dict(l=0, r=0, b=0, t=0),
            title="KMeans Model with PCA Feature Selection",
            #width=500,
            height=700,
        )
        #fig.show()

        #Group data Cluster averages
        data_done = data.copy()
        data_done['label'] = cons_data['label']
        data_avg = data_done.groupby(['label'], as_index=True).mean(numeric_only=True)
        data_avg = data_avg.drop("CustomerID", axis = 1)
        melted = data_avg.reset_index().melt(id_vars ="label")

        clust_fig = px.histogram(melted, x="label", y="value",
                 color='variable', barmode='group',
                 height=500, title = "Cluster Distribution With PCA")
        
    else:
        #Build Model
        sse = []

        for clust in range(1,10):
            kmeans = KMeans(n_clusters = clust, init = "k-means++")#n_jobs = -1, , init = "k-means++"
            print(f'136 cons_data: {cons_data}')
            kmeans.fit(cons_data)
            sse.append(kmeans.inertia_)

        #create dataframe
        cons_df = pd.DataFrame({"Cluster" : range(1,10), "SSE" : sse})

        #plot optimal k fig
        elbow_fig = px.line(cons_df, x='Cluster', y='SSE', markers=True,
                 title = 'Optimal K using Elbow Method')

        #Build models with optimal clusters
        kmeans = KMeans( n_clusters = optimal_k, init='k-means++') #n_jobs = -1,
        kmeans.fit(cons_data)

        sil = silhouette_score(cons_data, kmeans.labels_, metric='euclidean')
        
        clusters = kmeans.fit_predict(data.iloc[:,2:])
        cons_data["label"] = clusters

        #plot 3D fig
        fig = go.Figure(data=[go.Scatter3d(
            x=cons_data['Age'],
            y=cons_data['Annual Income (k$)'],
            z=cons_data['Spending Score (1-100)'],
            mode='markers',
            marker=dict(
                size=4,
                color=cons_data['label'],  # set color to an array/list of desired values
                colorscale='Viridis',   # choose a colorscale
                opacity=0.8
            ),
        )])

        # tight layout
        fig.update_layout(
            #margin=dict(l=0, r=0, b=0, t=0),
            title="KMeans Model without PCA Feature Selection",
            height=700
        )
        #fig.show()

        #Group data Cluster averages
        data_done = data.copy()
        data_done['label'] = cons_data['label']
        data_avg = data_done.groupby(['label'], as_index=True).mean(numeric_only=True)
        data_avg = data_avg.drop("CustomerID", axis = 1)
        melted = data_avg.reset_index().melt(id_vars ="label")

        clust_fig = px.histogram(melted, x="label", y="value",
                 color='variable', barmode='group',
                 height=500, title = "Cluster Distribution Without PCA")
    
    return elbow_fig, sil, fig, clust_fig


#==========================================================================================

def process_credit():
    data = pd.read_csv("assets/CC_GENERAL.csv")
    del(data["CUST_ID"])

    #Standardize Data
    cons = data.copy()
    scaler = StandardScaler().fit(cons.values)
    features = scaler.transform(cons.values)
    scaled_data = pd.DataFrame(features, columns = cons.columns).dropna()
    
    return scaled_data


def build_credit_model(cons_data, optimal_k, pca = False):
    
    org_data = pd.read_csv("assets/CC_GENERAL.csv")
    org_data = org_data.dropna()
    
    if pca:
        pca = PCA(n_components = len(cons_data.columns))
        principalComponents = pca.fit_transform(cons_data)

        feat = range(pca.n_components_)
        PCA_components = pd.DataFrame(principalComponents)
        
        rang = range(1, 10)
        inertias = []

        for ra in rang:
            model = KMeans(n_clusters= ra)
            model.fit(PCA_components.iloc[:,:1])
            inertias.append(model.inertia_)

        #create dataframe
        cons_df = pd.DataFrame({"Cluster" : range(1,10), "SSE" : inertias})
        
        #Plot Graph
        elbow_fig = make_subplots(rows=1, cols=2)
        
        #feature_selection
        elbow_fig.add_trace(
            go.Bar( x=list(feat), y=pca.explained_variance_ratio_.round(2),
                    text=pca.explained_variance_ratio_.round(2),
                    textposition='auto',
                ),
            row=1, col=1
        )
        
        #elbow
        elbow_fig.add_trace(
            go.Scatter(x=cons_df['Cluster'], y=cons_df['SSE'],
                            mode='markers+lines',
                            name='markers'),
            row=1, col=2
        )

        elbow_fig.update_layout(height=400, width=1200, title_text="Feature Selection and Optimal K selection using Elbow Method")

        #Build model with 4 cluster
        kmeans = KMeans(n_clusters = optimal_k)
        kmeans.fit(PCA_components)

        #Evaluate Model
        sil = silhouette_score(PCA_components, kmeans.labels_, metric='euclidean')
        
        clusters = kmeans.fit_predict(PCA_components)
        cons_data["label"] = clusters
        
        #plot 3D fig
        fig = go.Figure(data=[go.Scatter3d(
            x=cons_data['TENURE'],
            y=cons_data['BALANCE'],
            z=cons_data['CREDIT_LIMIT'],
            mode='markers',
            marker=dict(
                size=4,
                color=cons_data['label'],  # set color to an array/list of desired values
                colorscale='Viridis',   # choose a colorscale
                opacity=0.8
            ),
        )])

        # tight layout
        fig.update_layout(
            #margin=dict(l=0, r=0, b=0, t=0),
            title="KMeans Model with PCA Feature Selection",
            #width=500,
            height=700,
        )
        #fig.show()

        #Group data Cluster averages
        data_done = org_data.copy()
        data_done['label'] = cons_data['label']
        data_avg = data_done.groupby(['label'], as_index=True).mean(numeric_only=True)
        melted = data_avg.reset_index().melt(id_vars ="label")

        clust_fig = px.histogram(melted, x="label", y="value",
                 color='variable', barmode='group',
                 height=500, title = "Cluster Distribution With PCA")
        
    else:
        #Build Model
        sse = []

        for clust in range(1,10):
            kmeans = KMeans(n_clusters = clust, init = "k-means++")#n_jobs = -1, , init = "k-means++"
            kmeans.fit(cons_data)
            sse.append(kmeans.inertia_)

        #create dataframe
        cons_df = pd.DataFrame({"Cluster" : range(1,10), "SSE" : sse})

        #plot optimal k fig
        elbow_fig = px.line(cons_df, x='Cluster', y='SSE', markers=True,
                 title = 'Optimal K using Elbow Method')

        #Build models with optimal clusters
        kmeans = KMeans( n_clusters = optimal_k, init='k-means++') #n_jobs = -1,
        kmeans.fit(cons_data)

        sil = silhouette_score(cons_data, kmeans.labels_, metric='euclidean')
        
        clusters = kmeans.fit_predict(org_data.iloc[:,1:])
        cons_data["label"] = clusters

        #plot 3D fig
        fig = go.Figure(data=[go.Scatter3d(
            x=cons_data['TENURE'],
            y=cons_data['BALANCE'],
            z=cons_data['CREDIT_LIMIT'],
            mode='markers',
            marker=dict(
                size=4,
                color=cons_data['label'],  # set color to an array/list of desired values
                colorscale='Viridis',   # choose a colorscale
                opacity=0.8
            ),
        )])

        # tight layout
        fig.update_layout(
            #margin=dict(l=0, r=0, b=0, t=0),
            title="KMeans Model without PCA Feature Selection",
            height=700
        )
        #fig.show()

        #Group data Cluster averages
        data_done = org_data.copy()
        data_done['label'] = cons_data['label']
        data_avg = data_done.groupby(['label'], as_index=True).mean(numeric_only=True)
        #data_avg = data_avg.drop("CUST_ID", axis = 1)
        melted = data_avg.reset_index().melt(id_vars ="label")

        clust_fig = px.histogram(melted, x="label", y="value",
                 color='variable', barmode='group',
                 height=500, title = "Cluster Distribution Without PCA")
    
    return elbow_fig, sil, fig, clust_fig



