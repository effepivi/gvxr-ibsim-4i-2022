#jupyter \
#    nbconvert \
#    talk-IBSim-4i_2021_fvidal.ipynb \
#    --to markdown \
#    --TagRemovePreprocessor.remove_cell_tags no_markdown \
#    --output build/talk-IBSim-4i_2021_fvidal.md


#pandoc \
#    -o build/talk.tex \
#    build/talk-IBSim-4i_2021_fvidal.md

#--listings
#conda activate gvxr-ibsim-4i-2022
jupyter nbconvert --execute 01-Introduction-to-Xray-attenuation.ipynb --to slides --post serve

