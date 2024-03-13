import SwiftUI

struct PageAdjustView: View {

    @ObservedObject var viewModel: ViewModel 
    @State private var textActive = false
    
    var body: some View {
            
        VStack{
       
            VStack {
                Text("RIGHT SIDE").frame(height: 40)
            }
            .frame(maxWidth: .infinity)
            .background(Color.cyan)
            .font(.system(size: 18, weight: .black, design: .default))
                
            HStack{
                VStack(spacing: 5) {
                    Text("HIND: \(Int(viewModel.right_hind_leg_ini))")
                    Slider(value: $viewModel.right_hind_leg_ini, in: 80...100, step: 1.0, onEditingChanged:{bool in self.textActive = bool} )
                }
                VStack(spacing: 5) {
                    Text("FRONT: \(Int(viewModel.right_front_leg_ini))")
                    Slider(value: $viewModel.right_front_leg_ini, in: 80...100, step: 1.0, onEditingChanged:{bool in self.textActive = bool} )
                }
            }
                
            VStack {
                Text("LEFT SIDE").frame(height: 40)
            }
            .frame(maxWidth: .infinity)
            .background(Color.cyan)
            .font(.system(size: 18, weight: .black, design: .default))
                
            HStack{
                VStack(spacing: 5) {
                    Text("FRONT: \(Int(viewModel.left_front_leg_ini))")
                    Slider(value: $viewModel.left_front_leg_ini, in: 80...100, step: 1.0, onEditingChanged:{bool in self.textActive = bool} )
                }
                VStack(spacing: 5) {
                    Text("HIND: \(Int(viewModel.left_hind_leg_ini))")
                    Slider(value: $viewModel.left_hind_leg_ini, in: 80...100, step: 1.0, onEditingChanged:{bool in self.textActive = bool} )
                }
            }
                
            VStack {
                Button("UPDATE", action: {
                    viewModel.setAnglesInit()
                })
                .bold()
                .padding()
                .frame(width: 100, height: 50)
                .foregroundColor(Color.white)
                .background(Color.black)
                .cornerRadius(10)
            }
                
        }
        .padding()
            
    }
}
