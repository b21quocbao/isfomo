'use client';

import { useEffect, useState } from 'react';
import { usePathname, useRouter } from 'next/navigation';
import { IconAt, IconInfoSquareRoundedFilled } from '@tabler/icons-react';
import axios from 'axios';
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

const trumpCoinAddr = '0x0AB38A89CA6CC808cB255ECe2CCbf660d74ebeFe';
const dogeCoinAddr = '0xBdD620d44D64789b24173307A2FE29F0C4c423F0';

export const Predict = ({ param }: any) => {
  const [searchContent, setSearchContent] = useState(decodeURIComponent(param) ?? 'donald_trump');
  const router = useRouter();
  const pathname = usePathname();
  const p = pathname.substring(8);
  console.log(pathname.substring(8));

  const [responseData, setResponseData] = useState({
    news: [],
    score: 0,
  });
  const [error, setError] = useState(null);
  const [ste, setSte] = useState(0);
  const [newsList, setNewsList] = useState([]);
  const [showContent, setShowContent] = useState(false);

  const url = 'https://ethglobal2024.itdevwu.com/isfomo/STE';
  const dogeData = {
    start_date: '2024-09-13',
    end_date: '2024-09-19',
    asset_name: 'DOGE',
  };
  const trumpData = {
    start_date: '2024-09-13',
    end_date: '2024-09-19',
    asset_name: 'TrumpCoin',
  };
  const data = p === 'donald_trump' ? trumpData : dogeData;

  useEffect(() => {
    const handleSubmit = async () => {
      try {
        const response = await axios
          .post(url, data, {
            headers: {
              'Content-Type': 'application/json',
            },
            httpsAgent: new (require('https').Agent)({ rejectUnauthorized: false }), // To replicate the `-k` option
          })
          .then((response) => {
            console.log(response.data);
            setResponseData(response.data); // Store response data
          })
          .catch((error) => {
            console.error(error);
          });
        setError(null); // Clear any previous errors
      } catch (err) {
        // console.error('Error', err.message);
        // setError(err.message); // Set error message if request fails
        setResponseData(null as any); // Clear previous data on error
      }
    };
    handleSubmit(); // Call handleSubmit on mount
  }, []);

  const updateValue = () => {
    console.log(responseData);
    setSte(responseData.score);
    setNewsList(responseData.news);
    setShowContent(true);
  };

  const handleSearch = (e: any) => {
    e.preventDefault();
    router.push(`/search/${searchContent}`); // Navigate to the results page with the query
  };

  const handleChoose = (link: any) => {
    router.push(`/search/${link}`);
  };

  const lightBoxes = () => {
    const boxes = [];
    for (let i = 0; i < ste; i++) {
      boxes.push(
        <Box key={i} w={8} h={24} style={{ borderRadius: '2px', backgroundColor: '#878787' }} />
      );
    }
    return boxes;
  };
  const darkBoxes = () => {
    const boxes = [];
    for (let i = 0; i < 10 - ste; i++) {
      boxes.push(
        <Box key={i} w={8} h={24} style={{ borderRadius: '2px', backgroundColor: '#3d3d3d' }} />
      );
    }
    return boxes;
  };

  return (
    <MantineProvider theme={theme} defaultColorScheme="dark">
      <Stack w="49%" align="center">
        <Stack w="100%" p={50}>
          <Group justify="space-evenly">
            <Button
              color={p === 'donald_trump' ? '#5e5e5e' : '#3d3d3d'}
              w="30%"
              h={60}
              radius="sm"
              onClick={() => handleChoose('donald_trump')}
            >
              Donald Trump
            </Button>
            <Button
              color={p === 'elon_musk' ? '#5e5e5e' : '#3d3d3d'}
              w="30%"
              h={60}
              radius="sm"
              onClick={() => handleChoose('elon_musk')}
            >
              Elon Musk
            </Button>
            <Button color="#3d3d3d" w="30%" h={60} radius="sm" disabled>
              PEPE
            </Button>
            <Button color="#3d3d3d" w="30%" h={60} radius="sm" disabled>
              AIDOGE
            </Button>
            <Button color="#3d3d3d" w="30%" h={60} radius="sm" disabled>
              APE
            </Button>
            <Button color="#3d3d3d" w="30%" h={60} radius="sm" disabled>
              ...
            </Button>
          </Group>
          {(p === 'donald_trump' || p === 'elon_musk') && (
            <Group justify="center">
              <Button color="#5e5e5e" onClick={updateValue} w={200}>
                Get value
              </Button>
            </Group>
          )}
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
          {showContent && (
            <>
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
                  {ste >= 8 ? (
                    <img src="/mood-crazy-happy.svg" alt="LOGO SVG" width={36} height={36} />
                  ) : ste >= 5 ? (
                    <img src="/mood-smile.svg" alt="LOGO SVG" width={36} height={36} />
                  ) : ste >= 3 ? (
                    <img src="/mood-confuzed.svg" alt="LOGO SVG" width={36} height={36} />
                  ) : (
                    <img src="/mood-wrrr.svg" alt="LOGO SVG" width={36} height={36} />
                  )}

                  <Group gap={4}>
                    {lightBoxes()}
                    {darkBoxes()}
                  </Group>
                  <Text fw={600}>{ste + '/10'}</Text>
                </Group>
              </Group>
              <Stack mt={30}>
                <Text fw={700} size="lg">
                  Related token:
                </Text>
                <Group gap={0}>
                  <Text fw={600} ml={20}>
                    {p === 'donald_trump' ? 'TrumpCoin:' : 'DogeCoin:'}
                  </Text>
                  <Button
                    variant="transparent"
                    color="#fff"
                    size="sm"
                    onClick={() => {
                      if (p === 'donald_trump') {
                        window.open('https://arbiscan.io/token/' + trumpCoinAddr);
                      } else {
                        window.open('https://arbiscan.io/token/' + dogeCoinAddr);
                      }
                    }}
                  >
                    <Text fw={400} size="sm" td="underline">
                      {p === 'donald_trump' ? trumpCoinAddr : dogeCoinAddr}
                    </Text>
                  </Button>

                  <CopyButtonWrap link={p === 'donald_trump' ? trumpCoinAddr : dogeCoinAddr} />
                </Group>
              </Stack>
              <Stack mt={30}>
                <Text fw={700} size="lg">
                  Related news:
                </Text>
                <Stack ml={50} gap="xs">
                  {newsList &&
                    newsList.map((item: any, index) => (
                      <Group w="100%" align="flex-start" justify="space-between">
                        <Text fw={600} size="sm">{'No.' + (index + 1) + ':'}</Text>
                        <Stack w="85%" gap={0}>
                          <Text fw={400} size="sm">
                            {item.content}
                          </Text>
                          <Group justify="flex-end">
                            <Text fw={400} size="xs">{item.date}</Text>
                          </Group>
                        </Stack>
                      </Group>
                    ))}
                </Stack>
              </Stack>
            </>
          )}
        </Stack>
      </Stack>
    </MantineProvider>
  );
};
