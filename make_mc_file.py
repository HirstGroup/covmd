import argparse
import textwrap

def parse_input(input):

    with open(input) as infile:

        d = {}

        omit = []

        for line in infile:

            if line.startswith('OMIT_NAME'):
                omit = line.split()[1:]
                omit = [int(i) for i in omit]
                d['OMIT_NAME'] = omit

            if line.startswith('HEAD_NAME'):
                head = int(line.split()[1])
                d['HEAD_NAME'] = head

            if line.startswith('TAIL_NAME'):
                tail = int(line.split()[1])
                d['TAIL_NAME'] = tail

            if line.startswith('MAIN_CHAIN'):
                main_chain = int(line.split()[1])
                d['MAIN_CHAIN'] = main_chain


        print('OMIT', omit)
        print('HEAD', head)
        print('TAIL', tail)
        print('MAIN_CHAIN', main_chain)

    return d


def parse_mol2(input):

    d = {}

    with open(input) as infile:

        sel = False

        for line in infile:
            if '@<TRIPOS>BOND' in line:
                sel = False
            if sel:
                number = int(line.split()[0])
                name = line.split()[1]
                d[number] = name
            if '@<TRIPOS>ATOM' in line:
                sel = True

    return d


def make_mc_file(atom_number_name, parts, output, charge=0.0):

    parts = get_pre_head_post_tail(parts, atom_number_name)

    lines = []

    lines.append(f"HEAD_NAME {atom_number_name[parts['HEAD_NAME']]}")
    lines.append(f"TAIL_NAME {atom_number_name[parts['TAIL_NAME']]}")
    lines.append(f"MAIN_CHAIN {atom_number_name[parts['MAIN_CHAIN']]}")

    for atom in parts['OMIT_NAME']:
        lines.append(f'OMIT_NAME {atom_number_name[atom]}')

    lines.append(f"PRE_HEAD_TYPE {parts['PRE_HEAD_TYPE']}")
    lines.append(f"POST_TAIL_TYPE {parts['POST_TAIL_TYPE']}")
    lines.append(f'CHARGE {charge}')

    with open(output, 'w') as f:
        for line in lines:
            f.write(f'{line}\n')


    return lines


def get_pre_head_post_tail(parts, atom_number_name):

    if 'C' in atom_number_name[parts['HEAD_NAME']]:
        parts['PRE_HEAD_TYPE'] = 'N'
    elif 'N' in atom_number_name[parts['HEAD_NAME']]:
        parts['PRE_HEAD_TYPE'] = 'C'
    else:
        raise Exception('HEAD_NAME not C nor N')

    if 'N' in atom_number_name[parts['TAIL_NAME']]:
        parts['POST_TAIL_TYPE'] = 'C'
    elif 'C' in atom_number_name[parts['TAIL_NAME']]:
        parts['POST_TAIL_TYPE'] = 'N'
    else:
        raise Exception('TAIL_NAME not C nor N')

    return parts


def parse_input_mol2(input):
    """
    Get parts automatically from mol2 file by analysing residue names
    """

    with open(input) as f:
        lines = []
        sel = False
        for line in f:
            if '@<TRIPOS>BOND' in line: break
            if sel:
                lines.append(line)
            if '@<TRIPOS>ATOM' in line: sel = True
            

    omit_resnames = ['ASP', 'HIS']

    omit = []

    for line in lines:

        number = int(line.split()[0])
        name = line.split()[1]
        resname = line.split()[7][0:3]

        if resname in omit_resnames:
            omit.append(number)

        if resname == 'CYS' and name == 'N':
            head = number

        if resname == 'CYS' and name == 'C':
            tail = number

        if resname == 'CYS' and name == 'CA':
            main_chain = number

    d = {'OMIT_NAME': omit, 'HEAD_NAME': head, 'TAIL_NAME': tail, 'MAIN_CHAIN': main_chain}

    return d




if __name__ == '__main__':

    parser = argparse.ArgumentParser(description=textwrap.dedent('''
        Make MC file, can either use a TXT or MOL2 input 

        TXT Input file should contain
        OMIT_NAME list of atom numbers that will be ommited
        HEAD_NAME atom number that will be head, e.g. amide N or carbonyl C
        TAIL_NAME atom number that will be tail
        MAIN_CHAIN atom number connecting head and tail, usually alpha carbon

        MOL2 Input file should contain
        resnames for each residue (CYS, ASP, HIS)
        names for C, O and CA atoms in CYS that will be used for head, tail and main_chain
        '''), formatter_class=argparse.RawTextHelpFormatter)

    # required arguments
    parser.add_argument('-a','--aux', help='Auxiliary mol2 structure file with charges and Amber atom types', required=True)
    parser.add_argument('-i','--input', help='Input file', required=True)
    parser.add_argument('-fi','--format_input', help='Format of input file, txt or mol2', required=True)
    parser.add_argument('-o','--output', help='Output MC file', required=True)
    
    # optional arguments
    parser.add_argument('-c','--charge', type=float, help='Charge of molecule', default=0.0, required=False)

    args = parser.parse_args()

    if args.format_input.lower() == 'txt':
        parts = parse_input(args.input)
    elif args.format_input.lower() == 'mol2':
        parts = parse_input_mol2(args.input)
    else:
        sys.exit('Input format should either be txt or mol2')

    atom_number_name = parse_mol2(args.aux)

    parts = get_pre_head_post_tail(parts, atom_number_name)

    make_mc_file(atom_number_name, parts, args.output, charge=args.charge)



