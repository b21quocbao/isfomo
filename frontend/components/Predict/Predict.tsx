'use client';

import { useState } from 'react';
import { usePathname, useRouter } from 'next/navigation';
import { IconAt, IconInfoSquareRoundedFilled } from '@tabler/icons-react';
import {
  ActionIcon,
  Box,
  Button,
  createTheme,
  Group,
  Input,
  MantineProvider,
  rem,
  Stack,
  Text,
  Tooltip,
} from '@mantine/core';
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
  const [searchContent, setSearchContent] = useState(decodeURIComponent(param) ?? 'donald_trump');
  const router = useRouter();
  const pathname = usePathname();
  console.log(pathname.substring(8));
  const lightBoxes = Array.from({ length: 8 });
  const darkBoxes = Array.from({ length: 2 });

  const handleSearch = (e) => {
    e.preventDefault();
    router.push(`/search/${searchContent}`); // Navigate to the results page with the query
  };

  const handleChoose = (link) => {
    router.push(`/search/${link}`);
  };

  return (
    <MantineProvider theme={theme}>
      <Stack w="49%" align="center">
        <Stack w="100%" p={50}>
          <Group justify="space-evenly">
            <Button
              color={pathname.substring(8) === 'donald_trump' ? '#5e5e5e' : '#3d3d3d'}
              w="40%"
              h={80}
              radius="lg"
              onClick={() => handleChoose('donald_trump')}
            >
              Donald Trump
            </Button>
            <Button
              color={pathname.substring(8) === 'elon_musk' ? '#5e5e5e' : '#3d3d3d'}
              w="40%"
              h={80}
              radius="lg"
              onClick={() => handleChoose('elon_musk')}
            >
              Elon Musk
            </Button>
          </Group>
          {/* <Text size="lg" fw={700}>
            Is topic of{' '}
            <Text span td="underline" fw={900} size="xl">
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
          </Group> */}
          <Group mt={30} align="flex-start">
            <Text fw={700} size="lg">
              STE
              <Tooltip
                fw={600}
                arrowPosition="side"
                label={
                  <Text inherit>
                    STE(Short term emotion) is an integer ranging from 1 to 10, <br />
                    pointing out how popular the topic above is. <br />
                    (Higher means more popular)
                  </Text>
                }
                withArrow
                position="top-start"
                arrowSize={8}
                arrowOffset={20}
              >
                <ActionIcon variant="transparent" color="gray" onClick={() => {}}>
                  <IconInfoSquareRoundedFilled style={{ width: rem(16) }} />
                </ActionIcon>
              </Tooltip>
              :
            </Text>
            <Group gap="sm" align="center" ml={20}>
              <img src="/mood-crazy-happy.svg" alt="LOGO SVG" width={36} height={36} />
              <Group gap={4}>
                {lightBoxes.map((_, index) => (
                  <Box
                    key={index}
                    w={8}
                    h={24}
                    style={{ borderRadius: '2px', backgroundColor: '#878787' }}
                  />
                ))}
                {darkBoxes.map((_, index) => (
                  <Box
                    key={index}
                    w={8}
                    h={24}
                    style={{ borderRadius: '2px', backgroundColor: '#3d3d3d' }}
                  />
                ))}
              </Group>
              <Text fw={600}>8/10 FOMO!</Text>
            </Group>
          </Group>
          <Stack mt={30}>
            <Text fw={700} size="lg">
              Related token:
            </Text>
            <Stack ml={50} gap="xs">
              <Group>
                <Text fw={600}>Turbo:</Text>
                <Text fw={400} ml={50}>
                  0xa35923162c...431ad920d3
                </Text>
                <CopyButtonWrap link="0xa35923162c49cf95e6bf26623385eb431ad920d3" />
              </Group>
            </Stack>
          </Stack>
          <Stack mt={30}>
            <Text fw={700} size="lg">
              Related news:
            </Text>
            <Stack ml={50} gap="xs">
              <Group w="100%" align="flex-start" justify="space-between">
                <Text fw={600}>No.1:</Text>
                <Stack w="85%">
                  <Text fw={400}>
                    Donald Trump bought hamburgers for customers with Bitcoin in a bar named
                    'Pubkey'...
                  </Text>
                  <Group justify="flex-end">
                    <Text fw={400}>SEP 19, 2024, 08:02 AM</Text>
                  </Group>
                </Stack>
              </Group>
            </Stack>
          </Stack>
        </Stack>
      </Stack>
    </MantineProvider>
  );
};
