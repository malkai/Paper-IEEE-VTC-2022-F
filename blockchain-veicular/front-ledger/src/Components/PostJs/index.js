import React from 'react';
import { MainBox } from './style';

export const PostJs = ({posts, loading}) => {
    if(loading) {
        return <h2>Loading...</h2>
    }

    return(
        <>  <MainBox>
                <table className='w-full text-left border-2 border-solid border-black'>
                    <thead>
                        <tr className='bg-blue-700'>
                            <th className='text-black'>Fabricante</th>
                            <th className='text-black'>Co2 Emitido</th>
                            <th className='text-black'>Hash</th>
                            <th className='text-black'>VIM</th>
                        </tr>
                    </thead>
                    <tbody>
                        {posts.map(post => (
                            <tr key={post.id} className='border-2 border-solid border-black'>
                                <th scope='row' className='bg-blue-500'>
                                    {post.Fabricante}
                                </th>
                                <th scope='row'>
                                    {post.Co2Emitido}
                                </th>
                                <th scope='row' className='bg-blue-500'>
                                    {post.Hash}
                                </th>
                                <th scope='row'>
                                    {post.VIN}
                                </th>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </MainBox>
        </>
    )
};
