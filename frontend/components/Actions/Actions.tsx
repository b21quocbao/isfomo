'use client';

import { useState } from 'react';
import { IconCoinFilled, IconDirectionSignFilled, IconFountainFilled } from '@tabler/icons-react';
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

export const Actions = () => {
  const [tradeContent, setTradeContent] = useState('');
  const [showTool, setShowTool] = useState(false);
  const [isDeposit, setIsDeposit] = useState(true);
  return (
    <MantineProvider theme={theme}>
      <Stack w="49%" mt={showTool ? 0 : 100} align="center">
        <Stack w="100%" p={50} gap={30} align="center">
          <Stack align="flex-start">
            <Text size="lg" fw={700}>
              Token address:{' '}
              {showTool && (
                <Text w={400} inherit>
                  {tradeContent}
                </Text>
              )}
            </Text>
            <Input
              w={400}
              variant="filled"
              size="md"
              radius="md"
              value={tradeContent}
              onChange={(event) => setTradeContent(event.currentTarget.value)}
              placeholder="Input token address"
            />
          </Stack>
          <Group gap="xl">
            <Button
              variant="filled"
              radius="md"
              color="#5e5e5e"
              rightSection={<IconDirectionSignFilled size={18} />}
            >
              Go to Trade
            </Button>
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
                    <Button color="#5e5e5e" radius="md" variant="filled" w={200} rightSection={<IconFountainFilled size={18} />}>
                      Add Liquidity
                    </Button>
                  </Group>
                </>
              ) : (
                <>
                  <Group justify="center" mt="md">
                    <Button color="#5e5e5e" radius="md" variant="filled" w={150} rightSection={<IconCoinFilled size={18} />}>
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
