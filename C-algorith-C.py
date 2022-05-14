alpha = ['A', 'B', 'C', 'D']
beta = []

for a in alpha:
    for aa in alpha:
        if (a==aa) or ([a,aa] in beta) or ([aa,a] in beta):
            continue
        beta.append([a,aa])


for b in beta:
        print(b)
