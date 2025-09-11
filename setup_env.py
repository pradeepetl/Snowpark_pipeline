https://docs.snowflake.com/en/developer-guide/snowpark/python/setup

conda create --name py395_env --override-channels -c https://repo.anaconda.com/pkgs/snowflake python=3.9 numpy pandas pyarrow

#conda create --name py382_env --override-channels -c  python=3.8 numpy pandas pyarrow

conda init

conda activate py393_env

conda install snowflake-snowpark-python=1.5.0

pip install snowflake-snowpark-python==1.5.0

pip install snowflake -U

pip install snowflake-cli-labs


##################################### TROUBLESHOOTING #####################################
# sometime you may face certificate error. Just close the terminal or restart the kernel and run again.
# If you face certificate error, try below command
conda create --name py312_env --override-channels -c https://repo.anaconda.com/pkgs/snowflake python=3.12 numpy pandas pyarrow

conda init

conda install snowflake-snowpark-python
