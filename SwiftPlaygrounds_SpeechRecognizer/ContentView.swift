import SwiftUI

struct ContentView: View {
    @StateObject var speechRecognizer = SpeechRecognizer()
    @State private var isRecording = false
    
    var body: some View {
        VStack {
            Text(speechRecognizer.transcript)
                .padding()

            Button(action: {
                isRecording ? stop() : start()
            }) {
                Image(systemName: isRecording ? "mic.fill" : "mic.slash")
                    .foregroundStyle( isRecording ? .red : .blue)
                    .imageScale(.large)
                    .overlay(Circle()
                        .stroke( isRecording ? Color.red : Color.blue)
                        .frame(width: 30,height:30)
                    )
            }
        }
    }
    
}

private extension ContentView {

    private func start() {
        speechRecognizer.resetTranscript()
        speechRecognizer.startTranscribing()
        isRecording = true
    }

    private func stop() {
        speechRecognizer.stopTranscribing()
        isRecording = false
    }   

}