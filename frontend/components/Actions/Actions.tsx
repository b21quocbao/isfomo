'use client';

import { useCallback, useEffect, useState } from 'react';
import { usePathname } from 'next/navigation';
import { IconCoinFilled, IconDirectionSignFilled, IconFountainFilled } from '@tabler/icons-react';
import { useWeb3React } from '@web3-react/core';
import Web3 from 'web3';
import {
  Button,
  createTheme,
  Group,
  Input,
  MantineProvider,
  Select,
  Stack,
  Text,
} from '@mantine/core';
import abi from './abi.json';
import abi2 from './abi2.json';
import classes from '../input.module.css';

const theme = createTheme({
  components: {
    Input: Input.extend({
      classNames: {
        input: classes.input,
      },
    }),
  },
});

const trumpCoinAddr = '0x0AB38A89CA6CC808cB255ECe2CCbf660d74ebeFe';
const dogeCoinAddr = '0xBdD620d44D64789b24173307A2FE29F0C4c423F0';
const isFomoTrumpAddr = '0xcCA6763EBf014f220484e8716938302A8419b7Ed';
const isFomoDogeAddr = '0x139cccb9c02e6429041dedcf9c346005576c35ae';
const usdcAddr = '0x643923795B6467Ebc877747ceb7eB6C8d1093EfF';

export const Actions = () => {
  const [tradeContent, setTradeContent] = useState('');
  const [showTool, setShowTool] = useState(false);
  const [isDeposit, setIsDeposit] = useState(true);
  const [amount0, setAmount0] = useState('');
  const [amount1, setAmount1] = useState('');
  const [amount2, setAmount2] = useState('');
  const pathname = usePathname();
  const p = pathname.substring(8);
  const { account, isActive, connector } = useWeb3React();

  useEffect(() => {
    setTradeContent(p == 'donald_trump' ? trumpCoinAddr : dogeCoinAddr);
  }, [p]);

  const addLP = useCallback(() => {
    if (isActive && connector.provider) {
      const isFomoAddr = p == 'donald_trump' ? isFomoTrumpAddr : isFomoDogeAddr;
      const web3 = new Web3(connector.provider);
      const contract = new web3.eth.Contract(abi, isFomoAddr);
      const usdcToken = new web3.eth.Contract(abi2, usdcAddr);
      const memeCoin = new web3.eth.Contract(
        abi2,
        p == 'donald_trump' ? trumpCoinAddr : dogeCoinAddr
      );

      const callAddLP = async () => {
        try {
          await usdcToken.methods.approve(isFomoAddr, amount0).send({ from: account });
          await memeCoin.methods.approve(isFomoAddr, amount1).send({ from: account });
          await contract.methods
            .addLiquidity(BigInt(amount0) * BigInt(10 ** 6), BigInt(amount1) * BigInt(10 ** 18))
            .send({ from: account });
        } catch (error) {
          console.error('Error fetching token balance:', error);
        }
      };

      callAddLP();
    } else {
      alert('You must connect to your wallet first!');
    }
  }, [isActive, account, connector.provider, amount0, amount1, p]);

  const removeLP = useCallback(() => {
    if (isActive && connector.provider) {
      const isFomoAddr = p == 'donald_trump' ? isFomoTrumpAddr : isFomoDogeAddr;

      const web3 = new Web3(connector.provider);
      const contract = new web3.eth.Contract(abi, isFomoAddr);

      const callRemoveLP = async () => {
        try {
          await contract.methods.removeLiquidity(amount2).send({ from: account });
        } catch (error) {
          console.error('Error fetching token balance:', error);
        }
      };

      callRemoveLP();
    } else {
      alert('You must connect to your wallet first!');
    }
  }, [isActive, account, connector.provider, amount2, p]);

  return (
    <MantineProvider theme={theme} defaultColorScheme="dark">
      <Stack w="49%" mt={showTool ? 0 : 100} align="center">
        <Stack w="100%" p={50} gap={30} align="center">
          <Stack align="flex-start">
            <Text size="lg" fw={700}>
              Token address:{' '}
              {showTool && (
                <Text w={350} size="sm" fw={500}>
                  {tradeContent}
                </Text>
              )}
            </Text>
            <Group>
              <Input
                w={370}
                variant="filled"
                size="md"
                radius="md"
                value={tradeContent}
                onChange={(event) => setTradeContent(event.currentTarget.value)}
                placeholder="Input token address"
              />
              <Button
                variant="filled"
                radius="md"
                color="#5e5e5e"
                rightSection={<IconDirectionSignFilled size={18} />}
                onClick={() => {
                  if (p === 'donald trump') {
                    window.open(
                      'https://app.uniswap.org/#/swap?inputCurrency=ETH&outputCurrency=' +
                        trumpCoinAddr +
                        '&chain=arbitrum'
                    );
                  } else {
                    window.open(
                      'https://app.uniswap.org/#/swap?inputCurrency=ETH&outputCurrency=' +
                        dogeCoinAddr +
                        '&chain=arbitrum'
                    );
                  }
                }}
              >
                Go to Trade
              </Button>
            </Group>
          </Stack>
          <Group gap="xl">
            <Button
              variant="filled"
              radius="md"
              color="#5e5e5e"
              rightSection={<IconCoinFilled size={18} />}
              onClick={() => setShowTool(true)}
            >
              Uniswap LP Bot
            </Button>
          </Group>
          {showTool && (
            <Stack w="70%">
              <Group justify="center">
                <Button
                  size="md"
                  variant="transparent"
                  color={isDeposit ? '#fff' : 'dark'}
                  onClick={() => setIsDeposit(true)}
                >
                  Deposit
                </Button>
                <Button
                  size="md"
                  variant="transparent"
                  color={!isDeposit ? '#fff' : 'dark'}
                  onClick={() => setIsDeposit(false)}
                >
                  Withdraw
                </Button>
              </Group>
              {isDeposit ? (
                <>
                  <Group w="100%" justify="center">
                    <Input
                      w={200}
                      size="md"
                      radius="md"
                      placeholder="Input amount"
                      variant="filled"
                      value={amount1}
                      onChange={(e) => setAmount1(e.currentTarget.value)}
                    />
                    <Select
                      checkIconPosition="right"
                      data={['TrumpCoin']}
                      size="md"
                      w={150}
                      fw={500}
                      placeholder="Pick token pair"
                      defaultValue="TrumpCoin"
                    />
                  </Group>
                  <Group w="100%" justify="center">
                    <Input
                      w={200}
                      size="md"
                      radius="md"
                      placeholder="Input amount"
                      variant="filled"
                      value={amount0}
                      onChange={(e) => setAmount0(e.currentTarget.value)}
                    />
                    <Select
                      checkIconPosition="right"
                      data={['USDC']}
                      size="md"
                      w={150}
                      fw={500}
                      placeholder="Pick token pair"
                      defaultValue="USDC"
                    />
                  </Group>
                  <Group justify="center" mt="md">
                    <Button
                      color="#5e5e5e"
                      radius="md"
                      variant="filled"
                      w={200}
                      rightSection={<IconFountainFilled size={18} />}
                      onClick={() => addLP()}
                    >
                      Add Liquidity
                    </Button>
                  </Group>
                </>
              ) : (
                <>
                  <Input
                    w={200}
                    size="md"
                    radius="md"
                    placeholder="Input amount"
                    variant="filled"
                    value={amount2}
                    style={{
                      marginRight: 'auto',
                      marginLeft: 'auto',
                    }}
                    onChange={(e) => setAmount2(e.currentTarget.value)}
                  />
                  <Group justify="center" mt="md">
                    <Button
                      color="#5e5e5e"
                      radius="md"
                      variant="filled"
                      w={150}
                      rightSection={<IconCoinFilled size={18} />}
                      onClick={() => removeLP()}
                    >
                      Withdraw
                    </Button>
                  </Group>
                </>
              )}
            </Stack>
          )}
        </Stack>
      </Stack>
    </MantineProvider>
  );
};
