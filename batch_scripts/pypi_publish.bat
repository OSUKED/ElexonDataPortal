call cd ..
call conda activate BMRS2
call python setup.py sdist bdist_wheel
call twine upload --skip-existing dist/*
pause