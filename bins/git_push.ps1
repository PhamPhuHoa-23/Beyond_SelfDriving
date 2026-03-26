git init
git add .
git reset materials/images/part3/*
git reset materials/slides/*
git reset materials/images/*.ppm
git commit -m "Initialize project and add drivex_video scenes for Part 1-3"
git branch -M main
git remote add origin https://github.com/PhamPhuHoa-23/Beyond_SelfDriving.git
git push -u origin main -f
