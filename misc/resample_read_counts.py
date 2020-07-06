import argparse
import numpy as np
import pickle

def _resample_reads(data, depth):
  for vid, V in data['variants'].items():
    S = len(V['total_reads'])
    omega = V['omega_v']
    assert np.allclose(0.5, omega)

    V['total_reads'] = np.broadcast_to(depth, S)
    V['var_reads'] = np.random.binomial(n=depth, p=omega*V['phi'])
    V['ref_reads'] = V['total_reads'] - V['var_reads']
    V['vaf'] = V['var_reads'] / V['total_reads']

  return data

def _write_pickle(data, outfn):
  with open(outfn, 'wb') as F:
    pickle.dump(data, F)

def _write_ssm(data, outfn):
  header = ('id', 'name', 'var_reads', 'total_reads', 'var_read_prob', 'phi')
  _stringify = lambda arr: ','.join([str(val) for val in arr])

  with open(outfn, 'w') as F:
    print(*header, sep='\t', file=F)
    for vid, V in data['variants'].items():
      row = (
        vid,
        V['name'],
        _stringify(V['var_reads']),
        _stringify(V['total_reads']),
        _stringify(V['omega_v']),
        _stringify(V['phi']),
      )
      print(*row, sep='\t', file=F)

def main():
  parser = argparse.ArgumentParser(
    description='LOL HI THERE',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
  )
  parser.add_argument('--depth', type=int, default=100)
  parser.add_argument('pickle_file_in')
  parser.add_argument('pickle_file_out')
  parser.add_argument('ssm_file_out')
  args = parser.parse_args()

  with open(args.pickle_file_in, 'rb') as F:
    data = pickle.load(F)

  np.random.seed(data['seed'])
  _resample_reads(data, args.depth)
  _write_pickle(data, args.pickle_file_out)
  _write_ssm(data, args.ssm_file_out)

if __name__ == '__main__':
  main()
