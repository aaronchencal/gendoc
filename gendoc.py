from random import randint
from flask import Flask, request, render_template

class Tree:
    """
    >>> t = Tree(3, [Tree(2, [Tree(5)]), Tree(4)])
    >>> t.label
    3
    >>> t.branches[0].label
    2
    >>> t.branches[1].is_leaf()
    True
    """
    def __init__(self, label, branches=[]):
        for b in branches:
            assert isinstance(b, Tree)
        self.label = label
        self.branches = list(branches)

    def is_leaf(self):
        return not self.branches

    def map(self, fn):
        """
        Apply a function `fn` to each node in the tree and mutate the tree.

        >>> t1 = Tree(1)
        >>> t1.map(lambda x: x + 2)
        >>> t1.map(lambda x : x * 4)
        >>> t1.label
        12
        >>> t2 = Tree(3, [Tree(2, [Tree(5)]), Tree(4)])
        >>> t2.map(lambda x: x * x)
        >>> t2
        Tree(9, [Tree(4, [Tree(25)]), Tree(16)])
        """
        self.label = fn(self.label)
        for b in self.branches:
            b.map(fn)

    def __contains__(self, e):
        """
        Determine whether an element exists in the tree.

        >>> t1 = Tree(1)
        >>> 1 in t1
        True
        >>> 8 in t1
        False
        >>> t2 = Tree(3, [Tree(2, [Tree(5)]), Tree(4)])
        >>> 6 in t2
        False
        >>> 5 in t2
        True
        """
        if self.label == e:
            return True
        for b in self.branches:
            if e in b:
                return True
        return False

    def __repr__(self):
        if self.branches:
            branch_str = ', ' + repr(self.branches)
        else:
            branch_str = ''
        return 'Tree({0}{1})'.format(self.label, branch_str)

    # def __str__(self):
    #     def print_tree(t, indent=0):
    #         tree_str = '  ' * indent + str(t.label) + "\n"
    #         for b in t.branches:
    #             tree_str += print_tree(b, indent + 1)
    #         return tree_str
    #     return print_tree(self).rstrip()

def gen_tree(max_depth, label_start=0, label_end=20, subtreecount_start=2, subtreecount_end=6):
    rand_label = randint(label_start, label_end)
    if max_depth == 1:
        return Tree(rand_label)

    rand_subbies = randint(subtreecount_start, subtreecount_end)
    return Tree(rand_label, [gen_tree(max_depth - 1, label_start, label_end, subtreecount_start, subtreecount_end) for i in range(rand_subbies)])



app = Flask(__name__)
 
@app.route("/")
def my_form():
    return render_template('form.html')
 

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    ans = gen_tree(int(text))
    return render_template('form.html', ans=ans)

if __name__ == "__main__":
    app.run()






