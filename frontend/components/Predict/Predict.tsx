'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { IconAt } from '@tabler/icons-react';
import { Button, createTheme, Group, Input, MantineProvider, Stack, Text } from '@mantine/core';
import { CopyButtonWrap } from '../CopyButtonWrap/CopyButtonWrap';
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

export const Predict = ({ param }) => {
  const [searchContent, setSearchContent] = useState(decodeURIComponent(param) ?? '? ? ?');
  const router = useRouter();

  const handleSearch = (e) => {
    e.preventDefault();
    router.push(`/search/${searchContent}`); // Navigate to the results page with the query
  };

  return (
    <MantineProvider theme={theme}>
      <Stack w="49%" align="center">
        <Stack w="100%" p={50}>
          <Text size="lg" fw={700}>
            Is topic of{' '}
            <Text span inherit td="underline" fw={900}>
              {searchContent}
            </Text>{' '}
            FOMO?
          </Text>
          <Group w="100%" justify="space-between">
            <Input
              w="70%"
              variant="filled"
              size="md"
              radius="xl"
              value={searchContent}
              onChange={(event) => setSearchContent(event.currentTarget.value)}
              placeholder="Search name/event/address"
              leftSection={<IconAt size={20} />}
            />
            <Button variant="filled" size="md" radius="lg" color="#5e5e5e" onClick={handleSearch}>
              Search
            </Button>
          </Group>
          <Stack mt={30}>
            <Text fw={700} size="lg">
              Related token:
            </Text>
            <Stack ml={50} gap="xs">
              <Group>
                <Text fw={600}>Turbo: 0xa3592...920d3</Text>
                <CopyButtonWrap link="0xa35923162c49cf95e6bf26623385eb431ad920d3" />
              </Group>
            </Stack>
          </Stack>
          
        </Stack>
      </Stack>
    </MantineProvider>
  );
};
