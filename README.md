# group_II_intron
Python scripts for analyzing group II intron MD simulations

Reference: Zhao, Chen, et al. "Crystal structure of group II intron domain 1 reveals a template for RNA assembly." Nature chemical biology 11.12 (2015): 967-972.

### Adjust the residue index for average structures from MD simulation
```
python3 adjust_averagePDB.py --iso_input average.D1_iso.pdb --iso_output average.iso_adjusted.pdb --full_input average.D1_isofromfull.pdb --full_output average.full_adjusted.gro
```

### Adjust the residue index in the trajectories
```
python3 adjustGRO.py --iso_input D1_iso_traj.gro --iso_output iso_adjusted.gro --full_input D1_isofromfull_traj.gro --full_output full_adjusted.gro
```

### Calculate the pseudodihedral angle eta and theta from trajectories
```
python3 GetDihedral-FromGro.py --iso_input iso_adjusted.gro --full_input full_adjusted.gro
```
### Additional scripts for generating plots

Generate the plot of Delta from average structures: get_delta.ipynb

Calculate the visualize the distribution of pseudodihedral angles from trajectories: distribution_check.ipynb
