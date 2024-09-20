'use client';

import { useState } from 'react';
import { IconCoinFilled, IconDirectionSignFilled } from '@tabler/icons-react';
import { Button, createTheme, Group, Input, MantineProvider, Stack, Text } from '@mantine/core';
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
  return (
    <MantineProvider theme={theme}>
      <Stack w="49%" mt={100} align="center">
        <Stack w="100%" p={50} gap={30} align="center">
          <Group>
            <Text size="lg" fw={700}>
              Token address:
            </Text>
            <Input
              w="100%"
              variant="filled"
              size="md"
              radius="xl"
              value={tradeContent}
              onChange={(event) => setTradeContent(event.currentTarget.value)}
              placeholder="Input token address"
            />
          </Group>
          <Button
            variant="filled"
            size="md"
            radius="lg"
            color="#5e5e5e"
            rightSection={<IconDirectionSignFilled size={20} />}
          >
            Go to trade
          </Button>
          <Button
            variant="filled"
            size="md"
            radius="lg"
            color="#5e5e5e"
            rightSection={<IconCoinFilled size={20} />}
          >
            Uniswap LP Manager
          </Button>
        </Stack>
      </Stack>
    </MantineProvider>
  );
};
