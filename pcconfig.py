import pynecone as pc

class GfpanalysisConfig(pc.Config):
    pass

config = GfpanalysisConfig(
    app_name="gfp_analysis",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
)