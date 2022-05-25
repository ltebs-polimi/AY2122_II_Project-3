/*******************************************************************************
* File Name: MPU9250_ISR.h
* Version 1.70
*
*  Description:
*   Provides the function definitions for the Interrupt Controller.
*
*
********************************************************************************
* Copyright 2008-2015, Cypress Semiconductor Corporation.  All rights reserved.
* You may use this file only in accordance with the license, terms, conditions, 
* disclaimers, and limitations in the end user license agreement accompanying 
* the software package with which this file was provided.
*******************************************************************************/
#if !defined(CY_ISR_MPU9250_ISR_H)
#define CY_ISR_MPU9250_ISR_H


#include <cytypes.h>
#include <cyfitter.h>

/* Interrupt Controller API. */
void MPU9250_ISR_Start(void);
void MPU9250_ISR_StartEx(cyisraddress address);
void MPU9250_ISR_Stop(void);

CY_ISR_PROTO(MPU9250_ISR_Interrupt);

void MPU9250_ISR_SetVector(cyisraddress address);
cyisraddress MPU9250_ISR_GetVector(void);

void MPU9250_ISR_SetPriority(uint8 priority);
uint8 MPU9250_ISR_GetPriority(void);

void MPU9250_ISR_Enable(void);
uint8 MPU9250_ISR_GetState(void);
void MPU9250_ISR_Disable(void);

void MPU9250_ISR_SetPending(void);
void MPU9250_ISR_ClearPending(void);


/* Interrupt Controller Constants */

/* Address of the INTC.VECT[x] register that contains the Address of the MPU9250_ISR ISR. */
#define MPU9250_ISR_INTC_VECTOR            ((reg32 *) MPU9250_ISR__INTC_VECT)

/* Address of the MPU9250_ISR ISR priority. */
#define MPU9250_ISR_INTC_PRIOR             ((reg8 *) MPU9250_ISR__INTC_PRIOR_REG)

/* Priority of the MPU9250_ISR interrupt. */
#define MPU9250_ISR_INTC_PRIOR_NUMBER      MPU9250_ISR__INTC_PRIOR_NUM

/* Address of the INTC.SET_EN[x] byte to bit enable MPU9250_ISR interrupt. */
#define MPU9250_ISR_INTC_SET_EN            ((reg32 *) MPU9250_ISR__INTC_SET_EN_REG)

/* Address of the INTC.CLR_EN[x] register to bit clear the MPU9250_ISR interrupt. */
#define MPU9250_ISR_INTC_CLR_EN            ((reg32 *) MPU9250_ISR__INTC_CLR_EN_REG)

/* Address of the INTC.SET_PD[x] register to set the MPU9250_ISR interrupt state to pending. */
#define MPU9250_ISR_INTC_SET_PD            ((reg32 *) MPU9250_ISR__INTC_SET_PD_REG)

/* Address of the INTC.CLR_PD[x] register to clear the MPU9250_ISR interrupt. */
#define MPU9250_ISR_INTC_CLR_PD            ((reg32 *) MPU9250_ISR__INTC_CLR_PD_REG)


#endif /* CY_ISR_MPU9250_ISR_H */


/* [] END OF FILE */
