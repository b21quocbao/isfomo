'use client';

import { useEffect, useState } from 'react';
import { useWeb3React } from '@web3-react/core';
import { InjectedConnector } from '@web3-react/injected-connector';
import { Button, Group, Text } from '@mantine/core';

// Define Injected Connector for Sepolia network only
const injected = new InjectedConnector({
  supportedChainIds: [42161], // Sepolia Testnet Chain ID
});

export const Connect = () => {
  const { account, isActive, connector } = useWeb3React();

  // Connect to MetaMask
  const connectWallet = async () => {
    try {
      await connector.activate(injected);
    } catch (error) {
      console.error('Connection error', error);
    }
  };

  return (
    <Group justify="flex-end" p="xl">
      {!isActive ? (
        <Button variant="filled" size="md" radius="lg" color="#5e5e5e" onClick={connectWallet}>
          Connect
        </Button>
      ) : (
        <Text style={{ fontWeight: '600' }}>
          Connected as: {account?.slice(0, 7) + '...' + account?.slice(-5, -1)}
        </Text>
      )}
    </Group>
  );
};
