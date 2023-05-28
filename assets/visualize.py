import graphviz


def draw_net(config, genome, game=None, game_dir=None, view=True, filename=None, fmt='png'):
    """ Receives a genome and draws a neural network with arbitrary topology. """
    # If requested, use a copy of the genome which omits all components that won't affect the output.

    node_names = {}
    node_colors = {}
    assert type(node_names) is dict
    assert type(node_colors) is dict

    node_attrs = {
        'shape': 'circle',
        'height': '0.2',
        'width': '1',
        'color': 'orange',  # Make the outline of the nodes orange
        'fillcolor': 'black',  # Fill the nodes with black
        'style': 'filled',  # This is necessary to make fillcolor work
        'penwidth': '3.0',
    }

    graph_attrs = {
        'rankdir': 'LR',  # This will make the graph horizontal
        'ranksep': '2.5',
        'pad': '2',
        'bgcolor': 'black',
        'label': f'Trained {game} AI Neural Network',  # Add a title to the graph
        'fontcolor': 'white',
        'labelloc': 't',
        'fontsize': '40',
        'fontname': 'Sans',
    }

    dot = graphviz.Digraph(format=fmt, filename=f"../testings/ANN Diagram", node_attr=node_attrs, graph_attr=graph_attrs)

    inputs = set()
    for k in config.genome_config.input_keys:
        inputs.add(k)
        name = node_names.get(k, str(k))
        input_attrs = {'style': 'filled', 'shape': 'circle', 'fillcolor': node_colors.get(k, 'black')}
        dot.node(name, _attributes=input_attrs)

    outputs = set()
    for k in config.genome_config.output_keys:
        outputs.add(k)
        name = node_names.get(k, str(k))
        node_attrs = {'style': 'filled', 'fillcolor': node_colors.get(k, 'black')}
        dot.node(name, _attributes=node_attrs)

    for cg in genome.connections.values():
        if cg.enabled:
            # if cg.input not in used_nodes or cg.output not in used_nodes:
            #    continue
            input, output = cg.key
            a = node_names.get(input, str(input))
            b = node_names.get(output, str(output))
            style = 'solid'
            color = 'green' if cg.weight > 0 else 'red'
            width = str(1 + abs(cg.weight / 5.0))
            dot.edge(a, b, _attributes={'style': style, 'color': color, 'penwidth': width})

    dot.render(filename, directory=game_dir, view=view)

    return dot
