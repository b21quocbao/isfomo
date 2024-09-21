'use client';

import { Group, Stack, Text } from '@mantine/core';
import { Actions } from '@/components/Actions/Actions';
import { Connect } from '@/components/Connect/Connect';
import { Predict } from '@/components/Predict/Predict';

export const Hub = ({ param }: any) => {
  return (
    <Stack>
      <Group w="100%" justify="space-between" align="flex-start" pt={40} px={50}>
        <Group gap="xs">
          <img src="/mood-crazy-happy.svg" alt="LOGO SVG" width={36} height={36} />
          <Text size="xl" fw={900}>
            ISFOMO
          </Text>
        </Group>
        <Connect />
      </Group>
      <Group w="100%" justify="space-between" align="flex-start">
        <Predict param={param} />
        <Actions />
      </Group>
    </Stack>
  );
};
