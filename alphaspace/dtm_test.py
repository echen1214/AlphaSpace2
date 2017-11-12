import mdtraj,alphaspace


# initialize universe instance
universe = alphaspace.AS_Universe()
for i in range(1, 1 + 10):
    test_ligand_path = './tests/bcl2/lig/{}.pdb'.format(i)
    test_protein_path = './tests/bcl2/prot/{}.pdb'.format(i)
    ligand = mdtraj.load(test_ligand_path)
    protein = mdtraj.load(test_protein_path)

    universe.set_receptor(protein, append=True)
    universe.set_binder(ligand, append=True)



universe.run_alphaspace()


universe.config.screen_by_lig_cntct = True
universe.config.screen_by_face = False

universe.screen_pockets()

for i in range(universe.n_frames):
    for pocket in universe.pockets(snapshot_idx=i):
        print(
            pocket.total_score(5)
        )
