/* ========================================
 *
 * Copyright YOUR COMPANY, THE YEAR
 * All Rights Reserved
 * UNPUBLISHED, LICENSED SOFTWARE.
 *
 * CONFIDENTIAL AND PROPRIETARY INFORMATION
 * WHICH IS THE PROPERTY OF your company.
 *
 * ========================================
*/
#include <project.h>
#include <buttonled.h>

#define LED_ON 1
#define LED_OFF 0
#define DELAY 10
#define BUTTON_PRESSED 1

int x = 0;
uint8_t push_button_state; 

int Button_pushed() 
{
        push_button_state = PIN_BUTTON_Read(); 
        
        if (push_button_state == BUTTON_PRESSED) {
            
            while (x<5) {
                if(push_button_state == BUTTON_PRESSED) x++;
                else x=0;
                CyDelay(DELAY);             
            }
            
            if (x >= 5) PIN_LED_Write(LED_ON);
        }
        
       else if (push_button_state != BUTTON_PRESSED) {
                PIN_LED_Write(LED_OFF);
                x = 0;    
         }
    return 0;
}



/* [] END OF FILE */
