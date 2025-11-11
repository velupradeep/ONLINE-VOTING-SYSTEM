import pandas as pd
from pathlib import Path
import os

# path = Path("C:/Users/Desktop/Sem-5/CS301 CN/Project/Voting/database")
path = Path("database")

# Ensure database directory exists
path.mkdir(exist_ok=True)

def initialize_candidate_list():
    """Initialize candidate list with new parties if it doesn't exist"""
    cand_file = path / 'cand_list.csv'
    if not cand_file.exists():
        reset_cand_list()
        print("Candidate list initialized with new parties")

def count_reset():
    df=pd.read_csv(path/'voterList.csv')
    df=df[['voter_id','Name','Gender','Zone','City','Passw','hasVoted']]
    for index, row in df.iterrows():
        df['hasVoted'].iloc[index]=0
    df.to_csv(path/'voterList.csv')

    df=pd.read_csv(path/'cand_list.csv')
    df=df[['Sign','Name','Vote Count']]
    for index, row in df.iterrows():
        df['Vote Count'].iloc[index]=0
    df.to_csv (path/'cand_list.csv')


def reset_voter_list():
    df = pd.DataFrame(columns=['voter_id','Name','Gender','Zone','City','Passw','hasVoted'])
    df=df[['voter_id','Name','Gender','Zone','City','Passw','hasVoted']]
    df.to_csv(path/'voterList.csv')

def reset_cand_list():
    # Updated with new parties: DMK, ADMK, TVK instead of AAP and Shiv Sena
    df = pd.DataFrame({
        'Sign': ['bjp', 'cong', 'dmk', 'admk', 'tvk', 'nota'],
        'Name': ['BJP', 'Congress', 'DMK', 'ADMK', 'TVK', 'NOTA'],
        'Vote Count': [0, 0, 0, 0, 0, 0]
    })
    df=df[['Sign','Name','Vote Count']]
    df.to_csv(path/'cand_list.csv')
    print("Candidate list reset with new parties")


def verify(vid,passw):
    # Initialize candidate list on first run
    initialize_candidate_list()
    
    df=pd.read_csv(path/'voterList.csv')
    df=df[['voter_id','Passw','hasVoted']]
    for index, row in df.iterrows():
        if df['voter_id'].iloc[index]==vid and df['Passw'].iloc[index]==passw:
            return True
    return False


def isEligible(vid):
    df=pd.read_csv(path/'voterList.csv')
    df=df[['voter_id','Name','Gender','Zone','City','Passw','hasVoted']]
    for index, row in df.iterrows():
        if df['voter_id'].iloc[index]==vid and df['hasVoted'].iloc[index]==0:
            return True
    return False


def vote_update(st,vid):
    if isEligible(vid):
        df=pd.read_csv (path/'cand_list.csv')
        df=df[['Sign','Name','Vote Count']]
        for index, row in df.iterrows():
            if df['Sign'].iloc[index]==st:
                df['Vote Count'].iloc[index]+=1

        df.to_csv (path/'cand_list.csv')

        df=pd.read_csv(path/'voterList.csv')
        df=df[['voter_id','Name','Gender','Zone','City','Passw','hasVoted']]
        for index, row in df.iterrows():
            if df['voter_id'].iloc[index]==vid:
                df.loc[index, 'hasVoted'] = 1

        df.to_csv(path/'voterList.csv')

        return True
    return False


def show_result():
    # Initialize candidate list on first run
    initialize_candidate_list()
    
    df=pd.read_csv (path/'cand_list.csv')
    df=df[['Sign','Name','Vote Count']]
    v_cnt = {}
    for index, row in df.iterrows():
        v_cnt[df['Sign'].iloc[index]] = df['Vote Count'].iloc[index]
    return v_cnt


def taking_data_voter(name,gender,zone,city,passw):
    # Initialize candidate list on first run
    initialize_candidate_list()
    
    df=pd.read_csv(path/'voterList.csv')
    df=df[['voter_id','Name','Gender','Zone','City','Passw','hasVoted']]
    row,col=df.shape
    if row==0:
        vid = 10001
        df = pd.DataFrame({"voter_id":[vid],
                    "Name":[name],
                    "Gender":[gender],
                    "Zone":[zone],
                    "City":[city],
                    "Passw":[passw],
                    "hasVoted":[0]},)
    else:
        vid=df['voter_id'].iloc[-1]+1
        df1 = pd.DataFrame({"voter_id":[vid],
                    "Name":[name],
                    "Gender":[gender],
                    "Zone":[zone],
                    "City":[city],
                    "Passw":[passw],
                    "hasVoted":[0]},)

        df = pd.concat([df, df1],ignore_index=True)

    df.to_csv(path/'voterList.csv')

    return vid

# Initialize on import
initialize_candidate_list()