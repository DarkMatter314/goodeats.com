import { Metadata } from 'next'
import { UserCollections } from '@/components/UserCollections';

export const metadata: Metadata = {
  title: 'Goodeats | My Collections',
}

const Page: React.FC = () => {
  return (
    <UserCollections secret={process.env.JWT_SECRET as string} />
  )
}

export default Page
