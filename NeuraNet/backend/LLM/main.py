from transformers import AutoTokenizer
from petals import AutoDistributedModelForCausalLM

INITIAL_PEERS = [
    "/ip4/10.1.2.3/tcp/31234/p2p/QmcXhze98AcgGQDDYna23s4Jho96n8wkwLJv78vxtFNq44",
    "/ip4/10.1.2.4/tcp/31245/p2p/12D3KooWNPaCDFTKMKBkQazoznq2dkdD3jWkXnYCTJH8PFpggNM6",
]

model = AutoDistributedModelForCausalLM.from_pretrained("bigscience/bloom", initial_peers=INITIAL_PEERS)
