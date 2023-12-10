import streamlit as st #Web App 
# Streamlit Cloud - deployment
import time
import subprocess
from combined_news import combined_news
import os
import pandas as pd
from sklearn.decomposition import PCA #skicit-learn
from sentence_transformers import SentenceTransformer,util
import numpy as np
from tqdm import tqdm
from tqdm import trange
import json
import matplotlib.pyplot as plt
import torch

class SNS_FAILURE_ALERT(Exception):
       pass

#https://colab.research.google.com/drive/1-6FMSlHNIsrGh6foCsef0FcarMxnIuH7#scrollTo=gcyezYki4Fpj

analysis_allowed = False

st.set_page_config(
	page_title="APEX app",
	page_icon="🦅"
)

def display_props():
	st.title("SNS Platforms Failure Detection System") #title of web app
	st.columns([0.7,0.3])

display_props()

def load_data(file="daum_embedding-5.csv", labels="daum1118_full.csv"):
	"""Load data as csv file"""
	df = pd.read_csv(file)
	news_df = pd.read_csv(labels)
	data = df.values.tolist()
	labels = news_df['title'].values.tolist()
	return data, labels



def embed_text(filename):
	embeddings = []
	with st.spinner("""Generating embeddings for the data... Please wait."""):
		model = SentenceTransformer('sentence-transformers/use-cmlm-multilingual')
		with open(filename) as data:
			df = json.load(data)
			df = pd.DataFrame(df)
			for news,desc in tqdm(zip(df['title'],df['desc']), "Scrapping news"):
				print("news and desc:", news, desc)
				embedding = model.encode(news + desc)
				print("embedding shape:", embedding.shape)
				embedding = np.array(embedding, dtype=float).flatten()
				embeddings.append(embedding)
				if len(embeddings)%50 == 0:
					st.toast(f"Computed {len(embeddings)} out of {len(df['title'])}")
				if len(embeddings) == df.shape[0]:
					st.toast(f"Computed all: {df.shape[0]}")
					
			
			return pd.DataFrame(embeddings), df

def embed_text_bert(filename, top_k:int = -1, threshold:float = 0.2):
	embeddings = []
	with st.spinner("""Generating embeddings for the data... Please wait."""):
		model = SentenceTransformer('distiluse-base-multilingual-cased')
		df = pd.read_json(filename)
		fake = pd.DataFrame({'title':"카카오 모든 서비스 장애..이르면 밤 10시쯤 재개 예정", "desc":"[앵커] 오늘 오후부터 카카오톡 등 카카오 관련 모든 서비스가 중단됐습니다. 데이터센터 화재 때문인데 취재기자 연결해 자세한 내용 알아보겠습니다. 윤해리 기자! 데...","url":"https://v.daum.net/v/20221015224757214"}, index=[0]) 
		df = pd.concat([fake,fake5, pd.DataFrame(df)], ignore_index=True)
		# df = pd.DataFrame(df)
		news = (df['title'] + df['desc']).to_list()
		corpus_embeddings = model.encode(news, convert_to_tensor=True)			
		query_embeddings = model.encode(combined_news, convert_to_tensor=True)
		# We use cosine-similarity and torch.topk to find the highest 5 scores
		cos_scores = util.cos_sim(query_embeddings, corpus_embeddings)[0]
		large_score = cos_scores[cos_scores >= threshold] # threshold
		# print(large_score)
		if len(large_score) > 0:
			top_results = torch.topk(large_score, k=max(top_k, len(large_score)))
			# print(top_results)
			for score, idx in zip(top_results[0], top_results[1]):
				st.write(news[idx], "(Score: {:.4f})".format(score))
				st.write(df.iloc[int(idx), :])
				e = SNS_FAILURE_ALERT('FAILURE IS DETECTED!')
				st.exception(e)
				# st.markdown(news[idx], unsafe_allow_html=True)
		else:
			st.write("Absence of Failures Detected")

with st.container():
	# st.markdown("## News Scrapping ")
	# st.markdown("Collect breaking news from 25+ sources")
	if st.button("Analyze Now"): #make the button pretty and big
		st.info("Analyzing failure-related news in real-time...")
		thattime=f"Daum{int(time.time())}.json"
		with st.spinner("Analyzing... Hold on."):
			res = subprocess.run(["scrapy", "runspider", "spiders/daum.py",  "-O", thattime]) 
		st.toast("Downloaded latest news!")
		analysis_allowed=True
		filenames = [file for file in os.listdir() if os.path.isfile(file) and file.endswith('.json')]
		filename = max(filenames, key=os.path.getmtime)
		with open(filename) as data:
			df_origin = json.load(data)
			fake = pd.DataFrame({'title':"카카오 모든 서비스 장애..이르면 밤 10시쯤 재개 예정", "desc":"[앵커] 오늘 오후부터 카카오톡 등 카카오 관련 모든 서비스가 중단됐습니다. 데이터센터 화재 때문인데 취재기자 연결해 자세한 내용 알아보겠습니다. 윤해리 기자! 데...","url":"https://v.daum.net/v/20221015224757214"}, index=[0]) 
			fake5 = pd.DataFrame({'title':"내부 기술적 결함으로 인한 구글 정전", "desc":"구글은 월요일 전세계 서비스 중단이 자체 시스템 내부의 기술적 결함으로 인한 것임을 확인했습니다.", "url":"http:nnone"}, index=[1])

			df = pd.concat([fake, fake5, pd.DataFrame(df_origin)], ignore_index=True)
			st.toast(f"Scrapped news shape: {df.shape}")
			st.write(f"Scrapped news shape: {df.shape}")
			st.dataframe(df)
	

with st.container():
	if analysis_allowed:
		st.markdown("# Analysis Result")
		filenames = [file for file in os.listdir() if os.path.isfile(file) and file.endswith('.json')]
		filename = max(filenames, key=os.path.getmtime)
		embed_text_bert(filename)


st.markdown("---")
st.caption("by **APEX Team** for **EuclidSoft (유클리드소프트)** ")