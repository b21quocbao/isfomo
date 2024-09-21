'use client';

import {
  initializeConnector,
  useWeb3React,
  Web3ReactHooks,
  Web3ReactProvider,
} from '@web3-react/core';
import { MetaMask } from '@web3-react/metamask';

const [metaMask, hooks] = initializeConnector<MetaMask>((actions) => new MetaMask({ actions }));

const connectors: [MetaMask, Web3ReactHooks][] = [[metaMask, hooks]];

export default function EthereumProvider({ children }: { children: any }) {
  return <Web3ReactProvider connectors={connectors}>{children}</Web3ReactProvider>;
}
