/*******************************************************************************
* File Name: Connection_Led.h  
* Version 2.20
*
* Description:
*  This file contains Pin function prototypes and register defines
*
* Note:
*
********************************************************************************
* Copyright 2008-2015, Cypress Semiconductor Corporation.  All rights reserved.
* You may use this file only in accordance with the license, terms, conditions, 
* disclaimers, and limitations in the end user license agreement accompanying 
* the software package with which this file was provided.
*******************************************************************************/

#if !defined(CY_PINS_Connection_Led_H) /* Pins Connection_Led_H */
#define CY_PINS_Connection_Led_H

#include "cytypes.h"
#include "cyfitter.h"
#include "cypins.h"
#include "Connection_Led_aliases.h"

/* APIs are not generated for P15[7:6] */
#if !(CY_PSOC5A &&\
	 Connection_Led__PORT == 15 && ((Connection_Led__MASK & 0xC0) != 0))


/***************************************
*        Function Prototypes             
***************************************/    

/**
* \addtogroup group_general
* @{
*/
void    Connection_Led_Write(uint8 value);
void    Connection_Led_SetDriveMode(uint8 mode);
uint8   Connection_Led_ReadDataReg(void);
uint8   Connection_Led_Read(void);
void    Connection_Led_SetInterruptMode(uint16 position, uint16 mode);
uint8   Connection_Led_ClearInterrupt(void);
/** @} general */

/***************************************
*           API Constants        
***************************************/
/**
* \addtogroup group_constants
* @{
*/
    /** \addtogroup driveMode Drive mode constants
     * \brief Constants to be passed as "mode" parameter in the Connection_Led_SetDriveMode() function.
     *  @{
     */
        #define Connection_Led_DM_ALG_HIZ         PIN_DM_ALG_HIZ
        #define Connection_Led_DM_DIG_HIZ         PIN_DM_DIG_HIZ
        #define Connection_Led_DM_RES_UP          PIN_DM_RES_UP
        #define Connection_Led_DM_RES_DWN         PIN_DM_RES_DWN
        #define Connection_Led_DM_OD_LO           PIN_DM_OD_LO
        #define Connection_Led_DM_OD_HI           PIN_DM_OD_HI
        #define Connection_Led_DM_STRONG          PIN_DM_STRONG
        #define Connection_Led_DM_RES_UPDWN       PIN_DM_RES_UPDWN
    /** @} driveMode */
/** @} group_constants */
    
/* Digital Port Constants */
#define Connection_Led_MASK               Connection_Led__MASK
#define Connection_Led_SHIFT              Connection_Led__SHIFT
#define Connection_Led_WIDTH              1u

/* Interrupt constants */
#if defined(Connection_Led__INTSTAT)
/**
* \addtogroup group_constants
* @{
*/
    /** \addtogroup intrMode Interrupt constants
     * \brief Constants to be passed as "mode" parameter in Connection_Led_SetInterruptMode() function.
     *  @{
     */
        #define Connection_Led_INTR_NONE      (uint16)(0x0000u)
        #define Connection_Led_INTR_RISING    (uint16)(0x0001u)
        #define Connection_Led_INTR_FALLING   (uint16)(0x0002u)
        #define Connection_Led_INTR_BOTH      (uint16)(0x0003u) 
    /** @} intrMode */
/** @} group_constants */

    #define Connection_Led_INTR_MASK      (0x01u) 
#endif /* (Connection_Led__INTSTAT) */


/***************************************
*             Registers        
***************************************/

/* Main Port Registers */
/* Pin State */
#define Connection_Led_PS                     (* (reg8 *) Connection_Led__PS)
/* Data Register */
#define Connection_Led_DR                     (* (reg8 *) Connection_Led__DR)
/* Port Number */
#define Connection_Led_PRT_NUM                (* (reg8 *) Connection_Led__PRT) 
/* Connect to Analog Globals */                                                  
#define Connection_Led_AG                     (* (reg8 *) Connection_Led__AG)                       
/* Analog MUX bux enable */
#define Connection_Led_AMUX                   (* (reg8 *) Connection_Led__AMUX) 
/* Bidirectional Enable */                                                        
#define Connection_Led_BIE                    (* (reg8 *) Connection_Led__BIE)
/* Bit-mask for Aliased Register Access */
#define Connection_Led_BIT_MASK               (* (reg8 *) Connection_Led__BIT_MASK)
/* Bypass Enable */
#define Connection_Led_BYP                    (* (reg8 *) Connection_Led__BYP)
/* Port wide control signals */                                                   
#define Connection_Led_CTL                    (* (reg8 *) Connection_Led__CTL)
/* Drive Modes */
#define Connection_Led_DM0                    (* (reg8 *) Connection_Led__DM0) 
#define Connection_Led_DM1                    (* (reg8 *) Connection_Led__DM1)
#define Connection_Led_DM2                    (* (reg8 *) Connection_Led__DM2) 
/* Input Buffer Disable Override */
#define Connection_Led_INP_DIS                (* (reg8 *) Connection_Led__INP_DIS)
/* LCD Common or Segment Drive */
#define Connection_Led_LCD_COM_SEG            (* (reg8 *) Connection_Led__LCD_COM_SEG)
/* Enable Segment LCD */
#define Connection_Led_LCD_EN                 (* (reg8 *) Connection_Led__LCD_EN)
/* Slew Rate Control */
#define Connection_Led_SLW                    (* (reg8 *) Connection_Led__SLW)

/* DSI Port Registers */
/* Global DSI Select Register */
#define Connection_Led_PRTDSI__CAPS_SEL       (* (reg8 *) Connection_Led__PRTDSI__CAPS_SEL) 
/* Double Sync Enable */
#define Connection_Led_PRTDSI__DBL_SYNC_IN    (* (reg8 *) Connection_Led__PRTDSI__DBL_SYNC_IN) 
/* Output Enable Select Drive Strength */
#define Connection_Led_PRTDSI__OE_SEL0        (* (reg8 *) Connection_Led__PRTDSI__OE_SEL0) 
#define Connection_Led_PRTDSI__OE_SEL1        (* (reg8 *) Connection_Led__PRTDSI__OE_SEL1) 
/* Port Pin Output Select Registers */
#define Connection_Led_PRTDSI__OUT_SEL0       (* (reg8 *) Connection_Led__PRTDSI__OUT_SEL0) 
#define Connection_Led_PRTDSI__OUT_SEL1       (* (reg8 *) Connection_Led__PRTDSI__OUT_SEL1) 
/* Sync Output Enable Registers */
#define Connection_Led_PRTDSI__SYNC_OUT       (* (reg8 *) Connection_Led__PRTDSI__SYNC_OUT) 

/* SIO registers */
#if defined(Connection_Led__SIO_CFG)
    #define Connection_Led_SIO_HYST_EN        (* (reg8 *) Connection_Led__SIO_HYST_EN)
    #define Connection_Led_SIO_REG_HIFREQ     (* (reg8 *) Connection_Led__SIO_REG_HIFREQ)
    #define Connection_Led_SIO_CFG            (* (reg8 *) Connection_Led__SIO_CFG)
    #define Connection_Led_SIO_DIFF           (* (reg8 *) Connection_Led__SIO_DIFF)
#endif /* (Connection_Led__SIO_CFG) */

/* Interrupt Registers */
#if defined(Connection_Led__INTSTAT)
    #define Connection_Led_INTSTAT            (* (reg8 *) Connection_Led__INTSTAT)
    #define Connection_Led_SNAP               (* (reg8 *) Connection_Led__SNAP)
    
	#define Connection_Led_0_INTTYPE_REG 		(* (reg8 *) Connection_Led__0__INTTYPE)
#endif /* (Connection_Led__INTSTAT) */

#endif /* CY_PSOC5A... */

#endif /*  CY_PINS_Connection_Led_H */


/* [] END OF FILE */
