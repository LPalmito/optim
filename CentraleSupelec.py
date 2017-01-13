#!/usr/bin/env python3

# 2016 - Ecole Centrale Supélec - les élèves du cours d'optimisation et leur enseignant


import sys



class CSP:
    """Implémente un solveur de programmation par contraintes

    Utilisation:

    création d'une instance avec une liste d'ensemble. Le i-eme élément est le
    domaine de la i-ème variable.

    addConstraint(x, y, relation) ajoute une contrainte binaire entre la
    x-ième variable et la y-ième variable et relation est l'ensemble des
    couples de valeurs que peuvent prendre les variables.

    maintain_arc_consistency() demande au solveur de maintenir l'arc
    consistance. À appeler avant solve().

    start_trace(dotfile) demande au solveur de produire un fichier DOT avec
    l'arbre d'exploration. À appeler avant solve().

    end_trace() termine la production du fichier DOT.

    solve() est un itérateur sur les solutions.

    nodes contient le nombre de nœuds de l'arbre de recherche déjà visitées.
    """

    def __init__(self, domaines):
        """Crée un problème de satisfaction par contraintes
        avec n variables numérotés de 0 à n-1.

        :param domaines: liste d'ensembles. Les éléments des ensembles peuvent être de tout type.
        """
        n = len(domaines)
        self.var = range(n)
        self.dom = domaines
        self.conflict = [[] for x in self.var]
        self.assigned = [None] * n
        self.context = []
        self.nodes = 0
        self.print_tree = False
        self.maintain_AC = False
        # sanity check
        for y in self.var:
            for x in range(y):
                if self.dom[x] is self.dom[y]:
                    print("ERROR: variables %i and %i have the same domain object." % (x, y))
                    return
        sys.setrecursionlimit(max(sys.getrecursionlimit(), n + 10))
        self.dotfile = None


    def addConstraint(self, x, y, relation):
        """Ajoute une contrainte binaire sur le couple de variables x et y.
        :param x, y: identificateurs de variables entre 0 et n-1
        :param relation: ensemble de couple de valeurs u,v tel que
        l'affectation x := u, y := u satisfait la contrainte.
        (par abus de notation x est la variable et son indice).
        """
        assert x != y
        self.conflict[x].append((y, relation))
        self.conflict[y].append((x, {(v,u) for (u,v) in relation}))


    def maintain_arc_consistency(self):
        self.maintain_AC = True

    def solve(self):
        """Itérateur sur toutes les solutions.

        nodes contiendra à tout moment le nombre de nœuds de l'arbre d'exploration
        print_tree indique si solve() doit afficher une ligne par nœud de l'arbre
        maintain_AC indique si solve() doit maintenir l'arc consistance
        """
        self.nodes += 1
        x = self.selectVar()
        if self.dotfile:
            node = self.nodes
            print(' %i [label="%s"];' % (node, x), file=self.dotfile)
        if x is None:  # toutes les variables sont affectées
            yield self.assigned
        else:
            for u in self.dom[x]:
                self.assigned[x] = u
                history = self.save_context()
                Q = self.forward_check(x)
                if self.maintain_AC:        # établir la maintenance de l'arc constance si nécessaire
                    self.arc_consistency(Q)
                if self.dotfile:
                    label = "%s in %s" % (u, self.dom[x])
                    print(' %i -> %i [label="%s"];' % (node, self.nodes + 1, label), file=self.dotfile)
                for sol in self.solve():
                    yield sol
                self.restore_context(history)
                self.assigned[x] = None

    # --- gestion de contexte

    def save_context(self):
        return len(self.context)

    def restore_context(self, history):
        while len(self.context) > history:
            x, vals = self.context.pop()
            assert vals.isdisjoint(self.dom[x])
            self.dom[x] |= vals

    def remove_vals(self, x, vals):
        self.context.append((x, vals))
        assert self.assigned[x] == None
        assert vals <= self.dom[x]
        self.dom[x] -= vals

    # --- exploration

    def selectVar(self):
        """choisit une variable de branchement.
        Heuristique: choisir la variable au domaine minimal

        :returns: un indice de variable ou Npne, si toutes les variables sont affectées
        """
        choice = None
        for x in self.var:
            if self.assigned[x] is None and  \
               (choice is None or len(self.dom[x]) < len(self.dom[choice])):
               choice = x
        return choice

    def forward_check(self, x):
        """Effectue la vérification en avant après une affectation à x
        """
        u = self.assigned[x]
        Q = set()
        for y, rel in self.conflict[x]:
            if self.assigned[y] is None:
                to_remove = set()
                for v in self.dom[y]:
                    if (u, v) not in rel:
                        to_remove.add(v)
                if to_remove:
                    self.remove_vals(y, to_remove)
                    Q.add(y)
        return Q

    # --- arc consistance

    def arc_consistency(self, Q):
        """Le domaine des variables dans Q a été réduit.
        Maintenir l'arc consistance.
        Implémente l'algorithme AC3.
        """
        while Q:
            x = Q.pop()
            for y, relation in self.conflict[x]:
                if self.assigned[y] is None:
                    if self.revise(x, y, relation):
                        Q.add(y)


    def revise(self, x, y, relation):
        """le domaine de x vient d'être réduit.
        Vérifier si celui de y doit être réduit à son tour.
        :returns: True si le domaine de y a été réduit
        """
        to_remove = set()
        for v in self.dom[y]:
            if not self.hasSupport(y, v, x, relation):
                to_remove.add(v)
        self.remove_vals(y, to_remove)
        return to_remove

    def hasSupport(self, y, v, x, relation):
        """est-ce que l'affectation y := v a un support dans le domaine de x ?
        """
        for u in self.dom[x]:
            if (u, v) in relation:
                    return True
        return False

    # --- mettre une trace de l'arbre d'exploration dans un fichier

    def start_trace(self, filename="tmp.dot"):
        self.dotfile = open(filename, "w")
        print("digraph G {", file=self.dotfile)

    def end_trace(self):
        print("}", file=self.dotfile)
        self.dotfile.close()
        self.dotfile = None
