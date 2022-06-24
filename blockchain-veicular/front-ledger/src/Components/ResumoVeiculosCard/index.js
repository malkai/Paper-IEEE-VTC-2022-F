import React, { useState } from 'react';
import { Mainbox } from './style';
import { AiFillCar } from "react-icons/ai";
import { BsGearFill } from "react-icons/bs";
import { FaLeaf, FaMoneyBillWaveAlt } from "react-icons/fa";


function ResumoVeiculosCard(props) {
    return (
        <>
            <Mainbox>
                <div className='linha1'>
                    <div className='icon_text'>
                        {props.id === 0 ? 
                        <AiFillCar size={25}/> : ''}
                        {props.id === 1 ? 
                        <BsGearFill size={25}/> : ''}
                        {props.id === 2 ? 
                        <FaLeaf size={25}/> : ''}
                        {props.id === 3 ? 
                        <FaMoneyBillWaveAlt size={25}/> : ''}
                        <p>{props.texto}</p>
                    </div>
                    <div className='numero'>
                        <p>{props.quantidade}</p>
                    </div>
                </div>
            </Mainbox>
        </>
    );
}

export default ResumoVeiculosCard;