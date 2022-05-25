/*******************************************************************************
* File Name: PIN_BUTTON.h  
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

#if !defined(CY_PINS_PIN_BUTTON_H) /* Pins PIN_BUTTON_H */
#define CY_PINS_PIN_BUTTON_H

#include "cytypes.h"
#include "cyfitter.h"
#include "cypins.h"
#include "PIN_BUTTON_aliases.h"

/* APIs are not generated for P15[7:6] */
#if !(CY_PSOC5A &&\
	 PIN_BUTTON__PORT == 15 && ((PIN_BUTTON__MASK & 0xC0) != 0))


/***************************************
*        Function Prototypes             
***************************************/    

/**
* \addtogroup group_general
* @{
*/
void    PIN_BUTTON_Write(uint8 value);
void    PIN_BUTTON_SetDriveMode(uint8 mode);
uint8   PIN_BUTTON_ReadDataReg(void);
uint8   PIN_BUTTON_Read(void);
void    PIN_BUTTON_SetInterruptMode(uint16 position, uint16 mode);
uint8   PIN_BUTTON_ClearInterrupt(void);
/** @} general */

/***************************************
*           API Constants        
***************************************/
/**
* \addtogroup group_constants
* @{
*/
    /** \addtogroup driveMode Drive mode constants
     * \brief Constants to be passed as "mode" parameter in the PIN_BUTTON_SetDriveMode() function.
     *  @{
     */
        #define PIN_BUTTON_DM_ALG_HIZ         PIN_DM_ALG_HIZ
        #define PIN_BUTTON_DM_DIG_HIZ         PIN_DM_DIG_HIZ
        #define PIN_BUTTON_DM_RES_UP          PIN_DM_RES_UP
        #define PIN_BUTTON_DM_RES_DWN         PIN_DM_RES_DWN
        #define PIN_BUTTON_DM_OD_LO           PIN_DM_OD_LO
        #define PIN_BUTTON_DM_OD_HI           PIN_DM_OD_HI
        #define PIN_BUTTON_DM_STRONG          PIN_DM_STRONG
        #define PIN_BUTTON_DM_RES_UPDWN       PIN_DM_RES_UPDWN
    /** @} driveMode */
/** @} group_constants */
    
/* Digital Port Constants */
#define PIN_BUTTON_MASK               PIN_BUTTON__MASK
#define PIN_BUTTON_SHIFT              PIN_BUTTON__SHIFT
#define PIN_BUTTON_WIDTH              1u

/* Interrupt constants */
#if defined(PIN_BUTTON__INTSTAT)
/**
* \addtogroup group_constants
* @{
*/
    /** \addtogroup intrMode Interrupt constants
     * \brief Constants to be passed as "mode" parameter in PIN_BUTTON_SetInterruptMode() function.
     *  @{
     */
        #define PIN_BUTTON_INTR_NONE      (uint16)(0x0000u)
        #define PIN_BUTTON_INTR_RISING    (uint16)(0x0001u)
        #define PIN_BUTTON_INTR_FALLING   (uint16)(0x0002u)
        #define PIN_BUTTON_INTR_BOTH      (uint16)(0x0003u) 
    /** @} intrMode */
/** @} group_constants */

    #define PIN_BUTTON_INTR_MASK      (0x01u) 
#endif /* (PIN_BUTTON__INTSTAT) */


/***************************************
*             Registers        
***************************************/

/* Main Port Registers */
/* Pin State */
#define PIN_BUTTON_PS                     (* (reg8 *) PIN_BUTTON__PS)
/* Data Register */
#define PIN_BUTTON_DR                     (* (reg8 *) PIN_BUTTON__DR)
/* Port Number */
#define PIN_BUTTON_PRT_NUM                (* (reg8 *) PIN_BUTTON__PRT) 
/* Connect to Analog Globals */                                                  
#define PIN_BUTTON_AG                     (* (reg8 *) PIN_BUTTON__AG)                       
/* Analog MUX bux enable */
#define PIN_BUTTON_AMUX                   (* (reg8 *) PIN_BUTTON__AMUX) 
/* Bidirectional Enable */                                                        
#define PIN_BUTTON_BIE                    (* (reg8 *) PIN_BUTTON__BIE)
/* Bit-mask for Aliased Register Access */
#define PIN_BUTTON_BIT_MASK               (* (reg8 *) PIN_BUTTON__BIT_MASK)
/* Bypass Enable */
#define PIN_BUTTON_BYP                    (* (reg8 *) PIN_BUTTON__BYP)
/* Port wide control signals */                                                   
#define PIN_BUTTON_CTL                    (* (reg8 *) PIN_BUTTON__CTL)
/* Drive Modes */
#define PIN_BUTTON_DM0                    (* (reg8 *) PIN_BUTTON__DM0) 
#define PIN_BUTTON_DM1                    (* (reg8 *) PIN_BUTTON__DM1)
#define PIN_BUTTON_DM2                    (* (reg8 *) PIN_BUTTON__DM2) 
/* Input Buffer Disable Override */
#define PIN_BUTTON_INP_DIS                (* (reg8 *) PIN_BUTTON__INP_DIS)
/* LCD Common or Segment Drive */
#define PIN_BUTTON_LCD_COM_SEG            (* (reg8 *) PIN_BUTTON__LCD_COM_SEG)
/* Enable Segment LCD */
#define PIN_BUTTON_LCD_EN                 (* (reg8 *) PIN_BUTTON__LCD_EN)
/* Slew Rate Control */
#define PIN_BUTTON_SLW                    (* (reg8 *) PIN_BUTTON__SLW)

/* DSI Port Registers */
/* Global DSI Select Register */
#define PIN_BUTTON_PRTDSI__CAPS_SEL       (* (reg8 *) PIN_BUTTON__PRTDSI__CAPS_SEL) 
/* Double Sync Enable */
#define PIN_BUTTON_PRTDSI__DBL_SYNC_IN    (* (reg8 *) PIN_BUTTON__PRTDSI__DBL_SYNC_IN) 
/* Output Enable Select Drive Strength */
#define PIN_BUTTON_PRTDSI__OE_SEL0        (* (reg8 *) PIN_BUTTON__PRTDSI__OE_SEL0) 
#define PIN_BUTTON_PRTDSI__OE_SEL1        (* (reg8 *) PIN_BUTTON__PRTDSI__OE_SEL1) 
/* Port Pin Output Select Registers */
#define PIN_BUTTON_PRTDSI__OUT_SEL0       (* (reg8 *) PIN_BUTTON__PRTDSI__OUT_SEL0) 
#define PIN_BUTTON_PRTDSI__OUT_SEL1       (* (reg8 *) PIN_BUTTON__PRTDSI__OUT_SEL1) 
/* Sync Output Enable Registers */
#define PIN_BUTTON_PRTDSI__SYNC_OUT       (* (reg8 *) PIN_BUTTON__PRTDSI__SYNC_OUT) 

/* SIO registers */
#if defined(PIN_BUTTON__SIO_CFG)
    #define PIN_BUTTON_SIO_HYST_EN        (* (reg8 *) PIN_BUTTON__SIO_HYST_EN)
    #define PIN_BUTTON_SIO_REG_HIFREQ     (* (reg8 *) PIN_BUTTON__SIO_REG_HIFREQ)
    #define PIN_BUTTON_SIO_CFG            (* (reg8 *) PIN_BUTTON__SIO_CFG)
    #define PIN_BUTTON_SIO_DIFF           (* (reg8 *) PIN_BUTTON__SIO_DIFF)
#endif /* (PIN_BUTTON__SIO_CFG) */

/* Interrupt Registers */
#if defined(PIN_BUTTON__INTSTAT)
    #define PIN_BUTTON_INTSTAT            (* (reg8 *) PIN_BUTTON__INTSTAT)
    #define PIN_BUTTON_SNAP               (* (reg8 *) PIN_BUTTON__SNAP)
    
	#define PIN_BUTTON_0_INTTYPE_REG 		(* (reg8 *) PIN_BUTTON__0__INTTYPE)
#endif /* (PIN_BUTTON__INTSTAT) */

#endif /* CY_PSOC5A... */

#endif /*  CY_PINS_PIN_BUTTON_H */


/* [] END OF FILE */
