call cd ..
call conda env create -f environment.yml
call conda activate BMRS
call ipython kernel install --user --name=BMRS
pause