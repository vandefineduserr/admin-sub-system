"use client"
import {
  createStyles,
  Navbar,
  Avatar,
  UnstyledButton,
  Badge,
  rem,
} from '@mantine/core';

import {
  IconBulb,
  IconUser,
  IconCheckbox,
  IconSettings,
} from '@tabler/icons-react';

import { UserButton } from '../buttons/user-button';
import { useRouter } from 'next/navigation';
import { useLayoutEffect, useState } from 'react';
import { Me, Project } from '@/interfaces';
import myProfile from '@/services/me';
import workspace from '@/services/workspace';
import Link from 'next/link';

const DEFAULT = "https://images.unsplash.com/photo-1596434220574-9af8bf9a0891?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2928&q=808";

const useStyles = createStyles((theme) => ({
  navbar: {
    paddingTop: 0,
  },

  section: {
    marginLeft: `calc(${theme.spacing.md} * -1)`,
    marginRight: `calc(${theme.spacing.md} * -1)`,
    marginBottom: theme.spacing.md,

    '&:not(:last-of-type)': {
      borderBottom: `${rem(1)} solid ${
        theme.colorScheme === 'dark' ? theme.colors.dark[4] : theme.colors.gray[3]
      }`,
    },
  },

  searchCode: {
    fontWeight: 700,
    fontSize: rem(10),
    backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[7] : theme.colors.gray[0],
    border: `${rem(1)} solid ${
      theme.colorScheme === 'dark' ? theme.colors.dark[7] : theme.colors.gray[2]
    }`,
  },

  mainLinks: {
    paddingLeft: `calc(${theme.spacing.md} - ${theme.spacing.xs})`,
    paddingRight: `calc(${theme.spacing.md} - ${theme.spacing.xs})`,
    paddingBottom: theme.spacing.md,
  },

  mainLink: {
    display: 'flex',
    alignItems: 'center',
    width: '100%',
    fontSize: theme.fontSizes.xs,
    padding: `${rem(8)} ${theme.spacing.xs}`,
    borderRadius: theme.radius.sm,
    fontWeight: 500,
    color: theme.colorScheme === 'dark' ? theme.colors.dark[0] : theme.colors.gray[7],

    '&:hover': {
      backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[6] : theme.colors.gray[0],
      color: theme.colorScheme === 'dark' ? theme.white : theme.black,
    },
  },

  mainLinkInner: {
    display: 'flex',
    alignItems: 'center',
    flex: 1,
  },

  mainLinkIcon: {
    marginRight: theme.spacing.sm,
    color: theme.colorScheme === 'dark' ? theme.colors.dark[2] : theme.colors.gray[6],
  },

  mainLinkBadge: {
    padding: 0,
    width: rem(20),
    height: rem(20),
    pointerEvents: 'none',
  },

  collections: {
    paddingLeft: `calc(${theme.spacing.md} - ${rem(6)})`,
    paddingRight: `calc(${theme.spacing.md} - ${rem(6)})`,
    paddingBottom: theme.spacing.md,
  },

  collectionsHeader: {
    paddingLeft: `calc(${theme.spacing.md} + ${rem(2)})`,
    paddingRight: theme.spacing.md,
    marginBottom: rem(5),
  },

  collectionLink: {
    display: 'block',
    padding: `${rem(8)} ${theme.spacing.xs}`,
    textDecoration: 'none',
    borderRadius: theme.radius.sm,
    fontSize: theme.fontSizes.xs,
    color: theme.colorScheme === 'dark' ? theme.colors.dark[0] : theme.colors.gray[7],
    lineHeight: 1,
    fontWeight: 500,

    '&:hover': {
      backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[6] : theme.colors.gray[0],
      color: theme.colorScheme === 'dark' ? theme.white : theme.black,
    },
  },
}));



export default function NavbarNext({ ws }: { ws: string }) {
  const router = useRouter();
  const { classes } = useStyles();
  const [ myOwnProfile, setMyOwnProfile ] = useState<Me>();
  const [ collections, setCollections ] = useState<Project[]>()

  const links = [
    { icon: IconSettings, label: 'Проекты', goTo: `/${ws}` },
    { icon: IconCheckbox, label: 'Задачи', goTo: `/${ws}/tasks` },
    { icon: IconSettings, label: 'Настройки', goTo: `/${ws}/settings` },
  ];



  useLayoutEffect(() => { 
    const getMyOwnInfo = async () => {
      setMyOwnProfile((await myProfile.getMyInfo())?.data)
    }

    const getProjects = async () => {
      setCollections((await workspace.getWorkspaceInfo(ws)).data?.projectsDetails)
    }
    
    getMyOwnInfo()
    getProjects()

  }, [ws])

  const mainLinks = links.map((link) => (
    <UnstyledButton key={link.label} className={classes.mainLink} onClick={() => router.push(link.goTo)}>
      <div className={classes.mainLinkInner}>
        <link.icon size={20} className={classes.mainLinkIcon} stroke={1.5} />
        <span>{link.label}</span>
      </div>
    </UnstyledButton>
  ));

  const collectionLinks = collections !== undefined ? collections.map((collection: any) => (
    <Link
      href={`/${ws}/${collection.uid}`}
      key={collection.uid}
      className={`${classes.collectionLink} flex items-center`}
    >

      <Avatar 
        className='inline-flex'
        radius="xl"
        src={ collection.layout === "" ? DEFAULT : collection.layout } 
        style={{ marginRight: rem(9)}}
      >
        {collection.name[0]}

      </Avatar>
      <span className='inline-flex'> {collection.name} </span>
    </Link>
  )) : null;

  return (
    <Navbar height={700} width={{ sm: 300 }} p="md" className={`${classes.navbar} h-screen`}>
      <Navbar.Section className={classes.section} onClick={() => router.push('/me')}>
        <UserButton
          image="https://i.imgur.com/fGxgcDF.png"
          name={`${myOwnProfile?.firstname} ${myOwnProfile?.lastname}`}
          email={myOwnProfile?.email as string}
        />
      </Navbar.Section>

      <Navbar.Section className={classes.section}>
        <div className={classes.mainLinks}>{mainLinks}</div>
      </Navbar.Section>
      { collectionLinks !== undefined && (
        <Navbar.Section className={classes.section}>
          <div className={classes.collections}>{collectionLinks}</div>
        </Navbar.Section>
      )}
    </Navbar>
  );
}