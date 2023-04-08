import Image from 'next/image'
import Link from 'next/link'

interface AboutProps
{
    children?: React.ReactNode;
    Name: string;
    Role: string;
    ImagePath: string;
    Description: string;
    imageSize: number;
    GithubIds: string;
}


const About = ({children,Name,Role,ImagePath,Description,imageSize, GithubIds}:AboutProps) => {
    return (
    <div className='flex flex-col justify-center w-40' >
              <span><Image src={`${ImagePath}`} alt='Person' width={400} height={400} className={`h-${imageSize} object-cover`} />
              <h3 className='text-black text-center text-xl font-medium'>{Name}</h3>
              <p className='flex text-black text-center text-sm font-medium flex-wrap justify-center'> <strong>{Role}</strong> <br/> {Description} <br/>
              <Link className='font-light underline underline-offset-2 hover:underline-offset-1 hover:font-medium text-slate-600' href={'https://Github.com/'.concat(GithubIds.toString())}> {GithubIds}</Link>
              </p>
              </span>
              {children}
            </div>
    )

}

export default About;
