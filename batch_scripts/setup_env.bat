call cd ..
call conda env create -f environment.yml
call conda activate BMRS2
call ipython kernel install --user --name=BMRS2
pause