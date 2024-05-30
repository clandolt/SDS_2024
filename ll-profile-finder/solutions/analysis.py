
import pandas


if __name__ == "__main__":

    TARGET_PID = "AFH002"

    # read proposals
    proposals = pandas.read_csv("data-tables/Proposals.tsv", sep="\t")

    # print the relevant info
    print("Description:")
    print(proposals.loc[proposals["PID"] == TARGET_PID, "Description"].iloc[0])
    
    print("Requirements:")
    print(proposals.loc[proposals["PID"] == TARGET_PID, "Requirements"].iloc[0])
        
    print("Tech stack:")
    print(proposals.loc[proposals["PID"] == TARGET_PID, "Tech stack"].iloc[0])
    
    # expected profiles: 
    # - APA: Aditya Patel (migration experience),
    # - JSM: John Smith (migration experience),
    # - NDU: Nathan Dubois (4 years of GCP Solutions Architect)
